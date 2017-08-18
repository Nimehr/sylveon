import discord
from discord.ext import commands
from cogs.utils import checks
from __main__ import set_cog
from .utils.dataIO import dataIO
from .utils.chat_formatting import pagify, box
from __main__ import send_cmd_help, settings
from cogs.utils.dataIO import dataIO
from __main__ import send_cmd_help, set_cog
from subprocess import run as sp_run, PIPE
from asyncio import as_completed
from setuptools import distutils
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from time import time
from importlib.util import find_spec

import importlib
import traceback
import logging
import asyncio
import threading
import datetime
import glob
import os
import aiohttp
import shutil
from time import time

NUM_THREADS = 4
REPO_NONEX = 0x1
REPO_CLONE = 0x2
REPO_SAME = 0x4
REPOS_LIST = "https://twentysix26.github.io/Red-Docs/red_cog_approved_repos/"

DISCLAIMER = ("You're about to add a 3rd party repository. The creator of Red"
              " and its community have no responsibility for any potential "
              "damage that the content of 3rd party repositories might cause."
              "\nBy typing 'I agree' you declare to have read and understand "
              "the above message. This message won't be shown again until the"
              " next reboot.")

log = logging.getLogger("red.owner")


class CogNotFoundError(Exception):
    pass


class CogLoadError(Exception):
    pass


class NoSetupError(CogLoadError):
    pass


class CogUnloadError(Exception):
    pass


class OwnerUnloadWithoutReloadError(CogUnloadError):
    pass

class UpdateError(Exception):
    pass


class CloningError(UpdateError):
    pass


class RequirementFail(UpdateError):
    pass


class Owner:

    def __init__(self, bot):
        self.bot = bot
        self.setowner_lock = False
        self.file_path = "data/downloader/repos.json"
        self.disabled_commands = dataIO.load_json(self.file_path)
        self.session = aiohttp.ClientSession(loop=self.bot.loop)
        self.disclaimer_accepted = False
        self.path = "data/downloader/"
        self.repos = dataIO.load_json(self.file_path)
        self.executor = ThreadPoolExecutor(NUM_THREADS)
        self._do_first_run()

    def save_repos(self):
            dataIO.save_json(self.file_path, self.repos)

    def __unload(self):
        self.session.close()


    async def disable_commands(self):
        for cmd in self.disabled_commands:
            cmd_obj = await self.get_command(cmd)
            try:
                cmd_obj.enabled = False
                cmd_obj.hidden = True
            except:
                pass

    @commands.command(name = "l")
    @checks.serverowner_or_permissions(manage_server = True)
    async def load(self, *, cog_name: str):

        module = cog_name.strip()
        if "cogs." not in module:
            module = "cogs." + module
        try:
            self._load_cog(module)
        except CogNotFoundError:
            await self.bot.say("That cog could not be found.")
        except CogLoadError as e:
            log.exception(e)
            traceback.print_exc()
            await self.bot.say("There was an issue loading the cog. Check"
                               " your console or logs for more information.")
        except Exception as e:
            log.exception(e)
            traceback.print_exc()
            await self.bot.say('Cog was found and possibly loaded but '
                               'something went wrong. Check your console '
                               'or logs for more information.')
        else:
            set_cog(module, True)
            await self.disable_commands()
            await self.bot.say("The cog has been loaded.")

    @commands.group(invoke_without_command=True, name = "ul")
    @checks.serverowner_or_permissions(manage_server = True)
    async def unload(self, *, cog_name: str):

        module = cog_name.strip()
        if "cogs." not in module:
            module = "cogs." + module
        if not self._does_cogfile_exist(module):
            await self.bot.say("That cog file doesn't exist. I will not"
                               " turn off autoloading at start just in case"
                               " this isn't supposed to happen.")
        else:
            set_cog(module, False)
        try:
            self._unload_cog(module)
        except OwnerUnloadWithoutReloadError:
            await self.bot.say("I cannot allow you to unload the Owner plugin"
                               " unless you are in the process of reloading.")
        except CogUnloadError as e:
            log.exception(e)
            traceback.print_exc()
            await self.bot.say('Unable to safely unload that cog.')
        else:
            await self.bot.say("The cog has been unloaded.")

    @checks.serverowner_or_permissions(manage_server = True)
    @commands.command(name="re")
    async def _reload(self, *, cog_name: str):
        module = cog_name.strip()
        if "cogs." not in module:
            module = "cogs." + module

        try:
            self._unload_cog(module, reloading=True)
        except:
            pass

        try:
            self._load_cog(module)
        except CogNotFoundError:
            await self.bot.say("That cog cannot be found.")
        except NoSetupError:
            await self.bot.say("That cog does not have a setup function.")
        except CogLoadError as e:
            log.exception(e)
            traceback.print_exc()
            await self.bot.say("That cog could not be loaded. Check your"
                               " console or logs for more information.")
        else:
            set_cog(module, True)
            await self.disable_commands()
            await self.bot.say("The cog has been reloaded.")

    @commands.group(pass_context=True)
    @checks.serverowner_or_permissions(manage_server = True)
    async def c(self, ctx):
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @c.group(pass_context=True)
    async def repo(self, ctx):
        """Repo managment"""
        if ctx.invoked_subcommand is None or \
                isinstance(ctx.invoked_subcommand, commands.Group):
            await send_cmd_help(ctx)
            return

    @repo.command(name="add", pass_context=True)
    async def _repo_add(self, ctx, repo_name: str, repo_url: str):
        """Add a repository"""
        if not self.disclaimer_accepted:
            await self.bot.say(DISCLAIMER)
            answer = await self.bot.wait_for_message(timeout=30,
                                                     author=ctx.message.author)
            if answer is None:
                await self.bot.say('Not adding repo.')
                return
            elif "i agree" not in answer.content.lower():
                await self.bot.say('Not adding repo.')
                return
            else:
                self.disclaimer_accepted = True
        self.repos[repo_name] = {}
        self.repos[repo_name]['url'] = repo_url
        try:
            self.update_repo(repo_name)
        except CloningError:
            await self.bot.say("That repository link doesn't seem to be "
                               "valid.")
            del self.repos[repo_name]
            return
        self.populate_list(repo_name)
        self.save_repos()
        data = self.get_info_data(repo_name)
        if data:
            msg = data.get("INSTALL_MSG")
            if msg:
                await self.bot.say(msg[:2000])
        await self.bot.say("Repo '{}' added.".format(repo_name))

    @c.command(pass_context=True)
    async def update(self, ctx):
        """Updates cogs"""

        tasknum = 0
        num_repos = len(self.repos)

        min_dt = 0.5
        burst_inc = 0.1/(NUM_THREADS)
        touch_n = tasknum
        touch_t = time()

        def regulate(touch_t, touch_n):
            dt = time() - touch_t
            if dt + burst_inc*(touch_n) > min_dt:
                touch_n = 0
                touch_t = time()
                return True, touch_t, touch_n
            return False, touch_t, touch_n + 1

        tasks = []
        for r in self.repos:
            task = partial(self.update_repo, r)
            task = self.bot.loop.run_in_executor(self.executor, task)
            tasks.append(task)

        base_msg = "Downloading updated cogs, please wait... "
        status = ' %d/%d repos updated' % (tasknum, num_repos)
        msg = await self.bot.say(base_msg + status)

        updated_cogs = []
        new_cogs = []
        deleted_cogs = []
        failed_cogs = []
        error_repos = {}
        installed_updated_cogs = []

        for f in as_completed(tasks):
            tasknum += 1
            try:
                name, updates, oldhash = await f
                if updates:
                    if type(updates) is dict:
                        for k, l in updates.items():
                            tl = [(name, c, oldhash) for c in l]
                            if k == 'A':
                                new_cogs.extend(tl)
                            elif k == 'D':
                                deleted_cogs.extend(tl)
                            elif k == 'M':
                                updated_cogs.extend(tl)
            except UpdateError as e:
                name, what = e.args
                error_repos[name] = what
            edit, touch_t, touch_n = regulate(touch_t, touch_n)
            if edit:
                status = ' %d/%d repos updated' % (tasknum, num_repos)
                msg = await self._robust_edit(msg, base_msg + status)
        status = 'done. '

        for t in updated_cogs:
            repo, cog, _ = t
            if self.repos[repo][cog]['INSTALLED']:
                try:
                    await self.install(repo, cog,
                                       no_install_on_reqs_fail=False)
                except RequirementFail:
                    failed_cogs.append(t)
                else:
                    installed_updated_cogs.append(t)

        for t in updated_cogs.copy():
            if t in failed_cogs:
                updated_cogs.remove(t)

        if not any(self.repos[repo][cog]['INSTALLED'] for
                   repo, cog, _ in updated_cogs):
            status += ' No updates to apply. '

        if new_cogs:
            status += '\nNew cogs: ' \
                   + ', '.join('%s/%s' % c[:2] for c in new_cogs) + '.'
        if deleted_cogs:
            status += '\nDeleted cogs: ' \
                   + ', '.join('%s/%s' % c[:2] for c in deleted_cogs) + '.'
        if updated_cogs:
            status += '\nUpdated cogs: ' \
                   + ', '.join('%s/%s' % c[:2] for c in updated_cogs) + '.'
        if failed_cogs:
            status += '\nCogs that got new requirements which have ' + \
                   'failed to install: ' + \
                   ', '.join('%s/%s' % c[:2] for c in failed_cogs) + '.'
        if error_repos:
            status += '\nThe following repos failed to update: '
            for n, what in error_repos.items():
                status += '\n%s: %s' % (n, what)

        msg = await self._robust_edit(msg, base_msg + status)

        if not installed_updated_cogs:
            return

        patchnote_lang = 'Prolog'
        shorten_by = 8 + len(patchnote_lang)
        for note in self.patch_notes_handler(installed_updated_cogs):
            if note is None:
                continue
            for page in pagify(note, delims=['\n'], shorten_by=shorten_by):
                await self.bot.say(box(page, patchnote_lang))

        await self.bot.say("Cogs updated. Reload updated cogs? (yes/no)")
        answer = await self.bot.wait_for_message(timeout=15,
                                                 author=ctx.message.author)
        if answer is None:
            await self.bot.say("Ok then, you can reload cogs with"
                               " `{}reload <cog_name>`".format(ctx.prefix))
        elif answer.content.lower().strip() == "yes":
            registry = dataIO.load_json("data/red/cogs.json")
            update_list = []
            fail_list = []
            for repo, cog, _ in installed_updated_cogs:
                if not registry.get('cogs.' + cog, False):
                    continue
                try:
                    self.bot.unload_extension("cogs." + cog)
                    self.bot.load_extension("cogs." + cog)
                    update_list.append(cog)
                except:
                    fail_list.append(cog)
            msg = 'Done.'
            if update_list:
                msg += " The following cogs were reloaded: "\
                    + ', '.join(update_list) + "\n"
            if fail_list:
                msg += " The following cogs failed to reload: "\
                    + ', '.join(fail_list)
            await self.bot.say(msg)

        else:
            await self.bot.say("Ok then, you can reload cogs with"
                               " `{}reload <cog_name>`".format(ctx.prefix))

    @c.command(name="install", pass_context=True)
    async def _install(self, ctx, repo_name: str, cog: str):
        """Installs specified cog"""
        if repo_name not in self.repos:
            await self.bot.say("That repo doesn't exist.")
            return
        if cog not in self.repos[repo_name]:
            await self.bot.say("That cog isn't available from that repo.")
            return
        data = self.get_info_data(repo_name, cog)
        try:
            install_cog = await self.install(repo_name, cog, notify_reqs=True)
        except RequirementFail:
            await self.bot.say("That cog has requirements that I could not "
                               "install. Check the console for more "
                               "informations.")
            return
        if data is not None:
            install_msg = data.get("INSTALL_MSG", None)
            if install_msg:
                await self.bot.say(install_msg[:2000])
        if install_cog:
            await self.bot.say("Installation completed. Load it now? (yes/no)")
            answer = await self.bot.wait_for_message(timeout=15,
                                                     author=ctx.message.author)
            if answer is None:
                await self.bot.say("Ok then, you can load it with"
                                   " `{}load {}`".format(ctx.prefix, cog))
            elif answer.content.lower().strip() == "yes":
                set_cog("cogs." + cog, True)
                owner = self.bot.get_cog('Owner')
                await owner.load.callback(owner, cog_name=cog)
            else:
                await self.bot.say("Ok then, you can load it with"
                                   " `{}load {}`".format(ctx.prefix, cog))
        elif install_cog is False:
            await self.bot.say("Invalid cog. Installation aborted.")
        else:
            await self.bot.say("That cog doesn't exist. Use cog list to see"
                               " the full list.")

    async def install(self, repo_name, cog, *, notify_reqs=False,
                      no_install_on_reqs_fail=True):
        reqs_failed = False
        if cog.endswith('.py'):
            cog = cog[:-3]

        path = self.repos[repo_name][cog]['file']
        cog_folder_path = self.repos[repo_name][cog]['folder']
        cog_data_path = os.path.join(cog_folder_path, 'data')
        data = self.get_info_data(repo_name, cog)
        if data is not None:
            requirements = data.get("REQUIREMENTS", [])

            requirements = [r for r in requirements
                            if not self.is_lib_installed(r)]

            if requirements and notify_reqs:
                await self.bot.say("Installing cog's requirements...")

            for requirement in requirements:
                if not self.is_lib_installed(requirement):
                    success = await self.bot.pip_install(requirement)
                    if not success:
                        if no_install_on_reqs_fail:
                            raise RequirementFail()
                        else:
                            reqs_failed = True

        to_path = os.path.join("cogs/", cog + ".py")

        print("Copying {}...".format(cog))
        shutil.copy(path, to_path)

        if os.path.exists(cog_data_path):
            print("Copying {}'s data folder...".format(cog))
            distutils.dir_util.copy_tree(cog_data_path,
                                         os.path.join('data/', cog))
        self.repos[repo_name][cog]['INSTALLED'] = True
        self.save_repos()
        if not reqs_failed:
            return True
        else:
            raise RequirementFail()

    async def get_command(self, command):
        command = command.split()
        try:
            comm_obj = self.bot.commands[command[0]]
            if len(command) > 1:
                command.pop(0)
                for cmd in command:
                    comm_obj = comm_obj.commands[cmd]
        except KeyError:
            return KeyError
        for check in comm_obj.checks:
            if hasattr(check, "__name__") and check.__name__ == "is_owner_check":
                return False
        return comm_obj

    async def _robust_edit(self, msg, text):
        try:
            msg = await self.bot.edit_message(msg, text)
        except discord.errors.NotFound:
            msg = await self.bot.send_message(msg.channel, text)
        except:
            raise
        return msg

    def populate_list(self, name):
        valid_cogs = self.list_cogs(name)
        new = set(valid_cogs.keys())
        old = set(self.repos[name].keys())
        for cog in new - old:
            self.repos[name][cog] = valid_cogs.get(cog, {})
            self.repos[name][cog]['INSTALLED'] = False
        for cog in new & old:
            self.repos[name][cog].update(valid_cogs[cog])
        for cog in old - new:
            if cog != 'url':
                del self.repos[name][cog]

    def get_info_data(self, repo_name, cog=None):
        if cog is not None:
            cogs = self.list_cogs(repo_name)
            if cog in cogs:
                info_file = os.path.join(cogs[cog].get('folder'), "info.json")
                if os.path.isfile(info_file):
                    try:
                        data = dataIO.load_json(info_file)
                    except:
                        return None
                    return data
        else:
            repo_info = os.path.join(self.path, repo_name, 'info.json')
            if os.path.isfile(repo_info):
                try:
                    data = dataIO.load_json(repo_info)
                    return data
                except:
                    return None
        return None

    def update_repo(self, name):

        def run(*args, **kwargs):
            env = os.environ.copy()
            env['GIT_TERMINAL_PROMPT'] = '0'
            kwargs['env'] = env
            return sp_run(*args, **kwargs)

        try:
            dd = self.path
            if name not in self.repos:
                raise UpdateError("Repo does not exist in data, wtf")
            folder = os.path.join(dd, name)
            if not os.path.exists(os.path.join(folder, '.git')):
                url = self.repos[name].get('url')
                if not url:
                    raise UpdateError("Need to clone but no URL set")
                branch = None
                if "@" in url:
                    url, branch = url.rsplit("@", maxsplit=1)
                if branch is None:
                    p = run(["git", "clone", url, dd + name])
                else:
                    p = run(["git", "clone", "-b", branch, url, dd + name])
                if p.returncode != 0:
                    raise CloningError()
                self.populate_list(name)
                return name, REPO_CLONE, None
            else:
                rpcmd = ["git", "-C", dd + name, "rev-parse", "HEAD"]
                p = run(["git", "-C", dd + name, "reset", "--hard",
                        "origin/HEAD", "-q"])
                if p.returncode != 0:
                    raise UpdateError("Error resetting to origin/HEAD")
                p = run(rpcmd, stdout=PIPE)
                if p.returncode != 0:
                    raise UpdateError("Unable to determine old commit hash")
                oldhash = p.stdout.decode().strip()
                p = run(["git", "-C", dd + name, "pull", "-q", "--ff-only"])
                if p.returncode != 0:
                    raise UpdateError("Error pulling updates")
                p = run(rpcmd, stdout=PIPE)
                if p.returncode != 0:
                    raise UpdateError("Unable to determine new commit hash")
                newhash = p.stdout.decode().strip()
                if oldhash == newhash:
                    return name, REPO_SAME, None
                else:
                    self.populate_list(name)
                    self.save_repos()
                    ret = {}
                    cmd = ['git', '-C', dd + name, 'diff', '--no-commit-id',
                           '--name-status', oldhash, newhash]
                    p = run(cmd, stdout=PIPE)

                    if p.returncode != 0:
                        raise UpdateError("Error in git diff")

                    changed = p.stdout.strip().decode().split('\n')

                    for f in changed:
                        if not f.endswith('.py'):
                            continue

                        status, _, cogpath = f.partition('\t')
                        cogname = os.path.split(cogpath)[-1][:-3]
                        if status not in ret:
                            ret[status] = []
                        ret[status].append(cogname)

                    return name, ret, oldhash

        except CloningError as e:
            raise CloningError(name, *e.args) from None
        except UpdateError as e:
            raise UpdateError(name, *e.args) from None


    def format_patch(repo, cog, log):
        header = "Patch Notes for %s/%s" % (repo, cog)
        line = "=" * len(header)
        if log:
            return '\n'.join((header, line, log))



    def _load_cog(self, cogname):
        if not self._does_cogfile_exist(cogname):
            raise CogNotFoundError(cogname)
        try:
            mod_obj = importlib.import_module(cogname)
            importlib.reload(mod_obj)
            self.bot.load_extension(mod_obj.__name__)
        except SyntaxError as e:
            raise CogLoadError(*e.args)
        except:
            raise

    def _does_cogfile_exist(self, module):
        if "cogs." not in module:
            module = "cogs." + module
        if module not in self._list_cogs():
            return False
        return True

    def _list_cogs(self):
        cogs = [os.path.basename(f) for f in glob.glob("cogs/*.py")]
        return ["cogs." + os.path.splitext(f)[0] for f in cogs]

    def list_cogs(self, repo_name):
        valid_cogs = {}

        repo_path = os.path.join(self.path, repo_name)
        folders = [f for f in os.listdir(repo_path)
                   if os.path.isdir(os.path.join(repo_path, f))]
        legacy_path = os.path.join(repo_path, "cogs")
        legacy_folders = []
        if os.path.exists(legacy_path):
            for f in os.listdir(legacy_path):
                if os.path.isdir(os.path.join(legacy_path, f)):
                    legacy_folders.append(os.path.join("cogs", f))

        folders = folders + legacy_folders

        for f in folders:
            cog_folder_path = os.path.join(self.path, repo_name, f)
            cog_folder = os.path.basename(cog_folder_path)
            for cog in os.listdir(cog_folder_path):
                cog_path = os.path.join(cog_folder_path, cog)
                if os.path.isfile(cog_path) and cog_folder == cog[:-3]:
                    valid_cogs[cog[:-3]] = {'folder': cog_folder_path,
                                            'file': cog_path}
        return valid_cogs

    def _unload_cog(self, cogname, reloading=False):
        if not reloading and cogname == "cogs.owner":
            raise OwnerUnloadWithoutReloadError(
                "Can't unload the owner plugin :P")
        try:
            self.bot.unload_extension(cogname)
        except:
            raise CogUnloadError

    def _do_first_run(self):
        invalid = []
        save = False

        for repo in self.repos:
            broken = 'url' in self.repos[repo] and len(self.repos[repo]) == 1
            if broken:
                save = True
                try:
                    self.update_repo(repo)
                    self.populate_list(repo)
                except CloningError:
                    invalid.append(repo)
                    continue
                except Exception as e:
                    print(e)
                    continue

        for repo in invalid:
            del self.repos[repo]

        if save:
            self.save_repos()


def check_files():
    if not os.path.isfile("data/red/disabled_commands.json"):
        print("Creating empty disabled_commands.json...")
        dataIO.save_json("data/red/disabled_commands.json", [])

def check_folders():
    if not os.path.exists("data/downloader"):
        print('Making repo downloads folder...')
        os.mkdir('data/downloader')

def setup(bot):
    check_files()
    check_folders()
    n = Owner(bot)
    bot.add_cog(n)
