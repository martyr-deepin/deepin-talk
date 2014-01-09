import QtQuick 2.1
import QtGraphicalEffects 1.0
import QtQuick.Controls 1.0
import QtQuick.Controls.Styles 1.0
import QtQuick.Dialogs 1.0

import "../Widgets"
import "../scripts/common.js" as Common
import DTalk 1.0

DWindow {
    width: 600; height: 620
    property Item contentContainer

    onClosed: {
        contentContainer.destroy()
    }
    
    Component.onCompleted: {
        contentContainer = contentComponent.createObject(root)
    }
    
    Item {
        id: root
        anchors.fill: parent
        
        Component {
            id: contentComponent
            
            MessagePage {
                anchors.fill: parent
            }        
        }

    }
    
    
}