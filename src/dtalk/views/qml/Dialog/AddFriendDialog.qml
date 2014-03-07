import QtQuick 2.1
import "../Widgets" as Widgets

Widgets.DWindow {
    width: 300; height: 200
    visibleBackgroundImage: false
    backgoundColor: "#fff"
    visible: true
    titlebarButtons: titlebarClose
    titlebarLeftItem: Item {
        Row {
            
            spacing: 5
            anchors.left: parent.left            
            anchors.leftMargin: 10
            anchors.top: parent.top
            anchors.topMargin: 10
            Widgets.RoundImage {
                source: typeof(friend) == "undefined" ? "" : friend.avatar
                width: 22; height: 22
                anchors.verticalCenter: parent.verticalCenter
            }
            
            Text {
                text: typeof(friend) == "undefined" ? "" : friend.displayName
                anchors.verticalCenter: parent.verticalCenter
                color: "#573e99"
                font.underline: true
            }
            
            Text {
                anchors.verticalCenter: parent.verticalCenter
                text: "添加为好友"
            }

        }
    }
    
    Item {
        
        anchors.fill: parent
        anchors.top: parent.top
        anchors.topMargin: 10
        
        Rectangle {
            id: topSpliter
            color: "#bcbcbc"
            anchors.top: parent.top
            width: parent.width; height: 1 
        }
        
        Widgets.DTextArea {
            id: messageArea
            anchors.top: topSpliter.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            height: 100
            focus: true
            /* canPaste: false */
            selectByMouse: true
            selectByKeyboard: true
            
            Rectangle {
                anchors.fill: parent
                color: "#e1e1e1"
                z: -100
            }
        }
        
        Rectangle {
            id: bottomSpliter
            color: "#bcbcbc"
            anchors.top: messageArea.bottom
            width: parent.width; height: 1 
        }
        
        Item {
            id: buttonArea
            width: parent.width
            anchors.top: bottomSpliter.bottom
            anchors.bottom: parent.bottom
            
            Row {
                anchors.right: parent.right
                anchors.rightMargin: 10
                anchors.verticalCenter: parent.verticalCenter
                
                Rectangle {
                    radius: 12
                    border { width: 1; color: buttonArea.containsMouse ? "#573e99" : "#bcbcbc" }
                    width: sendButton.width + 4; height: sendButton.height + 2
                    color: buttonMouseArea.containsMouse ? "#573e99" : "#fff"
                    
                    Widgets.LayoutText {
                        id: sendButton
                        anchors.centerIn: parent
                        text: "发 送"
                        color: buttonMouseArea.containsMouse ? "#fff" : "#573e99"
                        font.pixelSize: 14
                        minWidth: 50
                        minHeight: 18
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    MouseArea {
                        id: buttonMouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: {
                            controlManager.requestAddFriend(friend.jid, messageArea.text)
                        }
                    }
                }
            }
        }
        
    }
}