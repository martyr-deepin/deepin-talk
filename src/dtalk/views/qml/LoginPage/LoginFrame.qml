import QtQuick 2.1
import QtQuick.Layouts 1.0
import "../Widgets" as Widgets
import DTalk 1.0

Item {
    id: container
    property alias isLogging: loginButton.isLogging
    
    function showErrorTip(text) {
        errorTip.show(text)
    }
    
    function loginUser() {
        serverManager.login(jidInput.text, passwd.text,  remember.checked, autoLogin.checked, "online")
    }
    
	Column {
		anchors.fill: parent
		anchors.topMargin: 90
		spacing: 50
		
		FaceFrame {
			width: parent.width
		}
        
		Column {
            z: 1000
			spacing: 10
			width: parent.width; height: 110

			LoginInput {
                id: jidInput
                property bool manualFlag: false
                property int lastLength: 0
				anchors.horizontalCenter: parent.horizontalCenter
				leftImage: "qrc:/images/common/person.png"
				rightImage: "qrc:/images/common/arrow.png"
                z: 1000
                
                onRightButtonClicked: {
                    accountCombo.visible = true
                }
                
                Keys.onDownPressed: {
                    if (accountCombo.visible) {
                        accountView.incrementCurrentIndex()
                    } else {
                        accountCombo.visible = true
                    }
                }
                Keys.onUpPressed: {
                    if (accountCombo.visible) {
                        accountView.decrementCurrentIndex()                            
                    } else {
                        accountCombo.visible = true
                    }

                }
                
                onReturnPressed: {
                    if (accountCombo.visible) {
                        accountView.setJid()
                    }
                }
                
                function setTextByManual(chars) {
                    manualFlag = true
                    text = chars
                    manualFlag = false
                }
                
                onInputFocusChanged: {
                    if (!focus) {
                        var temp = length
                        lastLength = temp
                    }
                }
                
                onLengthChanged: {
                    if (manualFlag) {
                        return
                    }
                    
                    if (lastLength >= length)  {
                        var temp = length
                        lastLength = temp
                        return 
                    } 
                    var temp = length
                    lastLength = temp
                    
                    if (length > 0) {
                        var obj = accountView.model.queryJid(text)
                        if (obj != undefined) {
                            setTextByManual(obj.jid)
                            textInput.select(obj.selStart, obj.selEnd)                                
                            if (obj.remember) {
                                passwd.text = obj.password
                            }
                        }
                    }
                }
                
                Widgets.DropRect {
                    id: accountCombo
                    anchors.top: parent.bottom
                    anchors.left: parent.left
                    anchors.leftMargin: -8
                    anchors.topMargin: -10
                    borderMargin: 0
                    rectRadius: 0
                    width: parent.width + sideWidth + 4
                    height: Math.max(accountView.contentHeight + sideWidth*2, 26+sideWidth*2)
                    visible: false
                    
                    PopupItem {
                        anchors.fill: parent
                        windowObject: windowView
                        parentObject: accountCombo
                    }
                    
                    Item  {
                        anchors.fill: parent
                        
                        Widgets.ScrollWidget {
                            anchors.fill: parent
                            ListView {
                                id: accountView
                                signal selected(string jid)
                                anchors.fill: parent
                                model: commonManager.getModel("userHistory")
                                delegate: AccountDelegate {}
                                
                                function hidePopup() {
                                    accountCombo.visible = false
                                }
                                onSelected: {
                                    jidInput.setTextByManual(jid)
                                }
                                
                                function setJid() {
                                    var obj = model.get(currentIndex)
                                    jidInput.setTextByManual(obj.jid)
                                    hidePopup()
                                }

                            }
                        }
                    }
                }
                
			}
			
			LoginInput {
                id: passwd
				anchors.horizontalCenter: parent.horizontalCenter
				leftImage: "qrc:/images/common/passwd.png"
				rightImage: "qrc:/images/common/keyboard.png"
				echoMode: TextInput.Password
                onReturnPressed: {
                    if (jidInput.text != "" & passwd.text != ""){
                        loginUser()
                        loginButton.isLogging = true
                    }
                    
                }
                
                Widgets.DTooltip { 
                    id: errorTip
                    anchors.top: parent.bottom
                    anchors.left: parent.left
                    anchors.topMargin: -20
                    anchors.leftMargin: -5
                    z: 100
                    visible: false
                }

                z: 10
			}
			
			Row {
				anchors.horizontalCenter: parent.horizontalCenter
				spacing: 35
				LoginStatus { height: 30 }
                
				Widgets.CheckBox {
                    id: remember
                    text: "记住密码"
                    onCheckedChanged: {
                        if (!checked) {
                            if (autoLogin.checked) {
                                autoLogin.checked = false
                            }
                        }
                    }
                }
                
				Widgets.CheckBox {
                    id: autoLogin;
                    text: "自动登录"
                    onCheckedChanged: {
                        if (checked) {
                            if (!remember.checked) {
                                remember.checked = true
                            }
                        }
                    }
                }
			}
		
		}
		
		LoginButton {
            id: loginButton
			width: parent.width
            onClicked: {
                if (jidInput.text != "" && passwd.text != ""){
                    loginUser()
                    isLogging = true
                } else {
                    showErrorTip("请输入密码")
                }
            }
		}
	}
}