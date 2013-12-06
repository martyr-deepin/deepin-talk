
function getDisplayName(instance) {
	if (instance.remark != "") {
		return instance.remark
	} else if (instance.nickname != "") {
		return instance.nickname
	} else {
		return instance.jid
	}
}

var ownerObj = modelManager.getModel("friend").getSelf()
