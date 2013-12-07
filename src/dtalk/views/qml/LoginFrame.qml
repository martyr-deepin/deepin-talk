import QtQuick 2.1
import QtQuick.Layouts 1.0

Item {
    id: container
    property alias isLogging: loginButton.isLogging
	
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
					leftImage: "image/person.png"
					rightImage: "image/arrow.png"
                    text: "houshao55@gmail.com"
				}
				
				LoginInput {
                    id: passwd
					anchors.horizontalCenter: parent.horizontalCenter
					leftImage: "image/passwd.png"
					rightImage: "image/keyboard.png"
					echoMode: TextInput.Password
				}
				
				Row {
					anchors.horizontalCenter: parent.horizontalCenter
					spacing: 35
					LoginStatus { height: 30 }
					CheckButton { text: "记住密码" }
					CheckButton { text: "自动登录" }
				}
		
			}
		
			LoginButton {
                id: loginButton
				width: parent.width
                onClicked: {
                    if (jid.text != "" & passwd.text != ""){
                        serverManager.login(jid.text, passwd.text)
                        isLogging = true
                    }
                }
			}
	}
	
	/* Row { */
	/* 	anchors.bottom: parent.bottom */
	/* 	LazyText { text: "注册帐号" } */
	/* 	LazyText { text: "忘记密码" } */
	/* } */
}