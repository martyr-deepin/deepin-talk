import QtQuick 2.1
import "../Widgets" as Widgets

Component {
    Item {
        id: wrapper
        property bool expend: wrapper.ListView.isCurrentItem
        width: wrapper.ListView.view.width; 
        height: expend ? control.height + friendView.contentHeight + 10 : control.height + 8
        
        Item {
            anchors.top: parent.top
            width: parent.width; height: Math.max(arrow.height, groupName.contentHeight)            
            id: control
            
            Row {
                anchors.fill: parent
                spacing: 10
                
                Image { 
                    id: arrow
                    source: "qrc:/images/common/arrow.png" 
                    anchors.verticalCenter: parent.verticalCenter
                    rotation: wrapper.expend ? 0 : -90
                }
                
                Widgets.GlowText { 
                    id: groupName
                    text: instance.name
                    /* color: "#fff" */
                    anchors.verticalCenter: parent.verticalCenter
                }
                
            }
            MouseArea {
                anchors.fill: parent
                hoverEnabled: true
                onClicked: {
                    wrapper.expend = !wrapper.expend
                }
            }
        }
            
        FriendView {
            anchors.topMargin: 20
            anchors.top: control.bottom
            anchors.bottom: parent.bottom
            width: parent.width
            visible: wrapper.expend
            id: friendView
            model: instance.friendModel
            interactive: false            
            clip: true
        }
    }
}