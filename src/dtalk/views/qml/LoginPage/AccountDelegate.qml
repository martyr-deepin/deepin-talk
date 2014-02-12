import QtQuick 2.1                            
import "../Widgets" as Widgets

Component {
    Item {
        id: wrapper
        width: wrapper.ListView.view.width
        height: 26
        
        Rectangle {
            anchors.fill: parent
            color: wrapper.ListView.view.currentIndex == index ? "#DBD1F3" : "#fff"
        }
        
        Text {
            width: parent.width - 8          
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 8
            text: instance.jid            

            color: wrapper.ListView.view.currentIndex == index ? "#000" : "#333"
            
            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                onContainsMouseChanged: {
                    if (containsMouse && wrapper.ListView.view.currentIndex != index) {
                        wrapper.ListView.view.currentIndex = index
                    }
                }
                onClicked: {
                    wrapper.ListView.view.hidePopup()
                    wrapper.ListView.view.selected(instance.jid)
                }
                
            }
        }
        
        Widgets.DButton {
            id: button
            source: "qrc:/images/common/small_close.png"
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: parent.right
            anchors.rightMargin: 10
            
            onClicked: {
                wrapper.ListView.view.model.removeByIndex(index)
            }
        }
        
    }
}                            

