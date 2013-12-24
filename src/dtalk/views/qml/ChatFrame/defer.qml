import QtQuick 2.1

Item {
    id: container
    
    Component.onCompleted: {
        var component = Qt.createComponent("ChatWindow.qml");
        object = component.createObject(container)
    }
}    
    