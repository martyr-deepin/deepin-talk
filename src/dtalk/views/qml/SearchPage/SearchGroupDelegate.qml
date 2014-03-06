import QtQuick 2.1
import "../Widgets" as Widgets

Component {
    Item {
        id: wrapper
        width: wrapper.ListView.view.width
        height: titleText.height + friendView.contentHeight + 10
        visible: instance.model.count > 0 ? true : false
                        
        Widgets.GlowText {
            id: titleText
            text: instance.title
        }
        
        LocalFriendDelegate { id: localFriendDelegate }
        RemoteFriendDelegate { id: remoteFriendDelegate }
        
        ListView {
            id: friendView
            anchors.top: titleText.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.topMargin: 10
            model: instance.model
            clip: true
            delegate: instance.type_ == "local" ? localFriendDelegate : remoteFriendDelegate
        }
        
    }
}
