#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 - 2019

import cmseekdb.basic as cmseek ## Good old module
import cmseekdb.result as sresult
import VersionDetect.outs as outsverdect
import time
import re



def _processURL(url,target):
	# add slash at the end of the URL
	if not url.endswith('/'):
		url += '/'
	
	# get the fully qualifeid domain name to recontruct URL
	fqdn = re.findall(r'https:\/\/(.*?)\/',url)

	# reconstruct url to specified target
	fullurl = 'https://' + str(fqdn[0]) + '/' + target + '/'

	return fullurl

def _checkUsers(url,ua):
	# Check Users eSpace for default credentials
	users = _processURL(url,'Users/Login.aspx')
	result = [False,'Users seems to not have default credentials.',users]
	test_source = cmseek.getsource(users,ua)
	
	if test_source[0] == '1':
		if 'Admin' in test_source[1] or 'admin' in test_source[1]:
			result = [True,'Users eSpace seems to have default credentials.',users]
	return result

def _checkSC(url,ua):
	scurl = _processURL(url,'ServiceCenter/Login.aspx')
	result = [False,'ServiceCenter seems to not be reachable',scurl]
	test_source = cmseek.getsource(scurl,ua)

	if test_source[0] == '1':
		if 'Welcome to the Service Center' in test_source[1]:
			result = [True,'ServiceCenter seems to be open to the world (or at least the IP from where you are scanning).',scurl]
		elif '403 - Forbidden' is test_source[1]:
			result = [False,'ServiceCenter seems to be protected by the Internal Network functionality.',scurl]
	return result		

def start(id, url, ua, ga, source, detection_method, headers):
	# Check users eSpace
	users = _checkUsers(url,ua)
	sc = _checkSC(url,ua)

	cmseek.clearscreen()
	cmseek.banner("CMS Scan Results")
	sresult.target(url)
	cms_version = outsverdect.start(id,source)
	sresult.cms('OutSystems',cms_version,'https://www.outsystems.com')
	sresult.init_item("Interesting findings" + cmseek.bold + cmseek.cln)
	sresult.init_sub(cmseek.bold + cmseek.fgreen + 'Users' + cmseek.cln, False)
	sresult.init_subsub("URL: " + cmseek.bold + cmseek.fgreen + users[2] + cmseek.cln, False, True)
	sresult.init_subsub(users[1] + cmseek.bold + cmseek.fgreen + cmseek.cln, False, True)
	sresult.init_sub(cmseek.bold + cmseek.fgreen + 'ServiceCenter' + cmseek.cln, False)
	sresult.init_subsub("URL: " + cmseek.bold + cmseek.fgreen + sc[2] + cmseek.cln, False, True)
	sresult.init_subsub(sc[1] + cmseek.bold + cmseek.fgreen + cmseek.cln, False, True)
	cmseek.update_log('cms_name', 'OutSystems') # update log
	if cms_version != '0' and cms_version != None:
		cmseek.update_log('cms_version', cms_version) # update log
	cmseek.update_log('cms_url', 'https://www.outsystems.com') # update log	
	cmseek.update_log('users_default_credentials',users[1])
	cmseek.update_log('users_url',users[2])
	cmseek.update_log('servicecenter_internal_network',sc[1])
	cmseek.update_log('servicecenter_url',sc[2])
	comptime = round(time.time() - cmseek.cstart, 2)
	log_dir = cmseek.log_dir
	if log_dir is not "":
		log_file = log_dir + "/cms.json"
	sresult.end(str(cmseek.total_requests), str(comptime), log_file)
	



	

if __name__ == '__main__':
	print(_processURL('https://igor-antunes.outsystemscloud.com','ServiceCenter'))
