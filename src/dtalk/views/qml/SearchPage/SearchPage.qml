import QtQuick 2.1
import "../Widgets" as Widgets

Item {
    id: root
    
    SearchBox {
        id: searchBox
        width: parent.width
        onLengthChanged: {
            view.model.doSearch(text)            
        }
    }
    
    Widgets.ScrollWidget {
        anchors.top: searchBox.bottom
        anchors.topMargin: 10
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        
        ListView {
            id: view
            anchors.fill: parent
            delegate: SearchGroupDelegate {}
            model: commonManager.getModel("searchGroup")
        }
    }
    
}