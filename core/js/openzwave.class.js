
/* This file is part of Jeedom.
 *
 * Jeedom is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Jeedom is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with Jeedom. If not, see <http://www.gnu.org/licenses/>.
 */


 jeedom.openzwave = function() {
 };

 jeedom.openzwave.durationConvert = function (d) {
 	d = Number(d);
 	var h = Math.floor(d / 3600);
 	var m = Math.floor(d % 3600 / 60);
 	var s = Math.floor(d % 3600 % 60);
 	return ((h > 0 ? h + " heure(s) " + (m < 10 ? "0" : "") : "") + m + " minute(s) " + (s < 10 ? "0" : "") + s) + ' seconde(s)';
 };

 jeedom.openzwave.timestampConverter = function (time) {
 	if (time == 1){
 		return "N/A";
 	}
 	var ret;
 	var date = new Date(time * 1000);
 	var hours = date.getHours();
 	if (hours < 10) {
 		hours = "0" + hours;
 	}
 	var minutes = date.getMinutes();
 	if (minutes < 10) {
 		minutes = "0" + minutes;
 	}
 	var seconds = date.getSeconds();
 	if (seconds < 10) {
 		seconds = "0" + seconds;
 	}
 	var num = date.getDate();
 	if (num < 10) {
 		num = "0" + num;
 	}
 	var month = date.getMonth() + 1;
 	if (month < 10) {
 		month = "0" + month;
 	}
 	var year = date.getFullYear();
 	var formattedTime = hours + ':' + minutes + ':' + seconds;
 	var formattedDate = num + "/" + month + "/" + year;
 	return formattedDate + ' ' + formattedTime;
 };

 jeedom.openzwave.normalizeClass = function (cc) {
 	if(typeof cc === 'string' && cc.indexOf('0x') >= 0){
 		return parseInt(cc,16)
 	}
 	return cc
 };

 /*************************Controller************************************************/

 jeedom.openzwave.controller = function() {
 };

 jeedom.openzwave.controller.action = function (_params) {
 	var paramsRequired = ['action'];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: 'controller/action('+_params.action+')',
 	};
 	$.ajax(paramsAJAX);
 }


 jeedom.openzwave.controller.addNodeToNetwork = function (_params) {
 	var paramsRequired = ['secure'];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: 'controller/addNodeToNetwork(1,'+_params.secure+')',
 	};
 	$.ajax(paramsAJAX);
 }

 jeedom.openzwave.controller.removeNodeFromNetwork = function (_params) {
 	var paramsRequired = [];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: 'controller/removeNodeFromNetwork(1)',
 	};
 	$.ajax(paramsAJAX);
 }

 jeedom.openzwave.controller.replicationSend = function (_params) {
 	var paramsRequired = [];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: 'controller/replicationSend('+_params.bridge_controller_id+')',
 	};
 	$.ajax(paramsAJAX);
 }

 /*************************Node************************************************/

 jeedom.openzwave.node = function() {
 };

 jeedom.openzwave.node.action = function (_params) {
 	var paramsRequired = ['action','node_id'];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: 'node/'+_params.node_id+'/action('+_params.action+')',
 	};
 	$.ajax(paramsAJAX);
 }

 jeedom.openzwave.node.info = function (_params) {
 	var paramsRequired = ['info','node_id'];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: 'node/'+_params.node_id+'/info('+_params.info+')',
 	};
 	$.ajax(paramsAJAX);
 }

 jeedom.openzwave.node.removeDeviceZWConfig = function (_params) {
 	var paramsRequired = ['node_id','all'];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: 'node/'+_params.node_id+'/removeDeviceZWConfig('+_params.all+')',
 	};
 	$.ajax(paramsAJAX);
 }

 jeedom.openzwave.node.refreshClass = function (_params) {
 	var paramsRequired = ['node_id','class'];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: 'node/'+_params.node_id+'/cc/'+jeedom.openzwave.normalizeClass(_params.class)+'/refreshClass()',
 	};
 	$.ajax(paramsAJAX);
 }

 jeedom.openzwave.node.dataClass = function (_params) {
 	var paramsRequired = ['node_id','class'];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: 'node/'+_params.node_id+'/cc/'+jeedom.openzwave.normalizeClass(_params.class)+'/data',
 	};
 	$.ajax(paramsAJAX);
 }

 jeedom.openzwave.node.refreshData = function (_params) {
 	var paramsRequired = ['node_id','instance','class','index'];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: '/node/'+_params.node_id+'/instance/'+_params.instance+'/cc/'+jeedom.openzwave.normalizeClass(_params.class)+'/index/'+_params.index+'/refreshData()',
 	};
 	$.ajax(paramsAJAX);
 }

 jeedom.openzwave.node.setPolling = function (_params) {
 	var paramsRequired = ['node_id','instance','class','index','polling'];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: '/node/'+_params.node_id+'/instance/'+_params.instance+'/cc/'+jeedom.openzwave.normalizeClass(_params.class)+'/index/'+_params.index+'/setPolling('+_params.polling+')',
 	};
 	$.ajax(paramsAJAX);
 }

 jeedom.openzwave.node.button = function (_params) {
 	var paramsRequired = ['node_id','instance','class','index','action'];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: '/node/'+_params.node_id+'/instance/'+_params.instance+'/cc/'+jeedom.openzwave.normalizeClass(_params.class)+'/index/'+_params.index+'/button('+_params.action+')',
 	};
 	$.ajax(paramsAJAX);
 }

 jeedom.openzwave.node.copyConfigurations = function (_params) {
 	var paramsRequired = ['node_id','target_id'];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: 'node/'+_params.node_id+'/copyConfigurations('+_params.target_id+')',
 	};
 	$.ajax(paramsAJAX);
 }


 jeedom.openzwave.node.setRaw = function (_params) {
 	var paramsRequired = ['node_id','slot_id','value'];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: 'node/'+_params.node_id+'/setRaw('+_params.slot_id+',['+_params.value+'])',
 	};
 	$.ajax(paramsAJAX);
 }

 jeedom.openzwave.node.set = function (_params) {
 	var paramsRequired = ['node_id','instance','class','index','value'];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: '/node/'+_params.node_id+'/instance/'+_params.instance+'/cc/'+jeedom.openzwave.normalizeClass(_params.class)+'/index/'+_params.index+'/set('+encodeURIComponent(_params.value)+')',
 	};
 	$.ajax(paramsAJAX);
 }

 jeedom.openzwave.node.setParam = function (_params) {
 	var paramsRequired = ['node_id','id','value','length'];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: '/node/'+_params.node_id+'/instance/0/cc/112/index/0/set('+_params.id+','+encodeURIComponent(_params.value)+','+_params.length+')',
 	};
 	$.ajax(paramsAJAX);
 }

 jeedom.openzwave.node.group = function (_params) {
 	var paramsRequired = ['node_id','group','target_id','instance','action'];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	_params.instance = _params.instance || 0
 	paramsAJAX.data = {
 		request: '/node/'+_params.node_id+'/'+_params.action+'('+_params.group+','+_params.target_id+','+_params.instance+')',
 	};
 	$.ajax(paramsAJAX);
 }


 /*************************Backup************************************************/

 jeedom.openzwave.backup = function() {
 };


 /*************************Backup************************************************/

 jeedom.openzwave.network = function() {
 };

 jeedom.openzwave.network.action = function (_params) {
 	var paramsRequired = ['action'];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: 'network/action('+_params.action+')',
 	};
 	$.ajax(paramsAJAX);
 }

 jeedom.openzwave.network.info = function (_params) {
 	var paramsRequired = ['info'];
 	var paramsSpecifics = {};
 	try {
 		jeedom.private.checkParamsRequired(_params || {}, paramsRequired);
 	} catch (e) {
 		(_params.error || paramsSpecifics.error || jeedom.private.default_params.error)(e);
 		return;
 	}
 	var params = $.extend({}, jeedom.private.default_params, paramsSpecifics, _params || {});
 	var paramsAJAX = jeedom.private.getParamsAJAX(params);
 	paramsAJAX.url = 'plugins/openzwave/core/php/jeeZwaveProxy.php';
 	paramsAJAX.data = {
 		request: 'network/info('+_params.info+')',
 	};
 	$.ajax(paramsAJAX);
 }