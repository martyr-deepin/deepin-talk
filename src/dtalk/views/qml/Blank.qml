import QtQuick 2.0

Rectangle {
    id: rect
    width: 80; height: 80
    color: "red"
    
    Rectangle {
        id: testRect
        anchors.fill: parent
        color: "green"
    }

    NumberAnimation on opacity {
        to: 0
        duration: 1000

        onRunningChanged: {
            if (!running) {
                console.log("Destroying...")
                /* rect.destroy(); */
                testRect.destroy()
            }
        }
    }
}