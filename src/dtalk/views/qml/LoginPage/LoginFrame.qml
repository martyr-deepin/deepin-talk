import QtQuick 2.1
import QtQuick.Layouts 1.0
import "../Widgets"

Item {
    id: container
    property alias isLogging: loginButton.isLogging
    
    function showErrorTip(text) {
        errorTip.show(text)
    }
    
	Column {
			anchors.fill: parent
			anchors.topMargin: 90
			spacing: 50
		
			FaceFrame {
				width: parent.width
			}
		
			Column {
				spacing: 10
				width: parent.width; height: 110

				LoginInput {
                    id: jid
					anchors.horizontalCenter: parent.horizontalCenter
					leftImage: "qrc:/images/common/person.png"
					rightImage: "qrc:/images/common/arrow.png"
				}
				
				LoginInput {
                    id: passwd
					anchors.horizontalCenter: parent.horizontalCenter
					leftImage: "qrc:/images/common/passwd.png"
					rightImage: "qrc:/images/common/keyboard.png"
					echoMode: TextInput.Password
                    onReturnPressed: {
                        if (jid.text != "" & passwd.text != ""){
                            serverManager.login(jid.text, passwd.text)
                            loginButton.isLogging = true
                        }
                        
                    }
                    
                    DTooltip { 
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
					CheckBox { text: "记住密码" }
					CheckBox { text: "自动登录" }
				}
		
			}
		
			LoginButton {
                id: loginButton
				width: parent.width
                onClicked: {
                    if (jid.text != "" && passwd.text != ""){
                        serverManager.login(jid.text, passwd.text)
                        isLogging = true
                    } else {
                        showErrorTip("请输入密码")
                    }
                }
			}
	}
}