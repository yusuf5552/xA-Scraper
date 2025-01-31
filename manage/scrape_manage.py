

import flags
import traceback
import os.path

import logSetup
from settings import settings

import signal
import time
import multiprocessing
import multiprocessing.managers
import sys

from . import cli_utils

manager = multiprocessing.managers.SyncManager()
manager.start()
namespace = manager.Namespace()
namespace.run = True

from main import JOBS
from main import JOBS_DISABLED

PLUGINS_ALL = {
		key : (cls_def, cls_def.pluginName)
	for cls_def, dummy_interval, key in JOBS + JOBS_DISABLED
}

ENABLED_PLUGINS = {
		key : (cls_def, cls_def.pluginName)
	for cls_def, dummy_interval, key in JOBS
}


def do_plugin(requested_name):
	if requested_name not in PLUGINS_ALL:
		print("Cannot find plugin for name %s!" % requested_name)
		return

	plg, dummy_name = PLUGINS_ALL[requested_name]

	if hasattr(plg, "runScraper"):
		plg.runScraper(namespace)
	else:
		print()
		print("Missing run command:", plg)
		print()
	# instance.go(ctrlNamespace=namespace)

def do_fetch(args):
	print("fetch args", args, type(args))
	if len(args) == 0:
		print("Fetching for all sites!")
		keys = list(ENABLED_PLUGINS.keys())
		keys.sort()
		for key in keys:
			if not namespace.run:
				return
			try:
				do_plugin(key)
			except Exception as e:
				traceback.print_exc()
	else:
		for plgname in args:
			if not plgname in PLUGINS_ALL:
				print("Error! Plugin short-name '%s' is not known!" % plgname)

		for plgname in args:
			do_plugin(plgname)



def do_fetch_all():

	processes = [
			multiprocessing.Process(target=do_plugin, name='run-'+key, args=(key, ))
		for
			key in PLUGINS.keys()
	]

	# Start all the plugins
	[tmp.start() for tmp in processes]

	while any([tmp.is_alive() for tmp in processes]):
		time.sleep(5)
		status = {tmp.name : tmp.is_alive() for tmp in processes}
		print("Plugin status: ", status)




