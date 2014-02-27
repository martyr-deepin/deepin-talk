import QtQuick 2.1

FocusScope {
    id: focusScope
    width: 250; height: 28
    property string placeholder    
    property alias text: textInput.text
    property alias length: textInput.length
    
    signal clicked

    Rectangle {
        color: "transparent"
        width: parent.width; height: parent.height
    }

    Rectangle {
        color: "transparent"
        width: parent.width; height: parent.height
        border { width: 1; color: "#333"}
        visible: parent.activeFocus ? true : false
    }

    Text {
        id: typeSomething
        anchors.fill: parent; anchors.leftMargin: 8
        verticalAlignment: Text.AlignVCenter
        text: placeholder
        color: "gray"
        font.italic: true
    }

    MouseArea { 
        anchors.fill: parent
        onClicked: { focusScope.focus = true }
    }

    TextInput {
        id: textInput
        anchors { left: parent.left; leftMargin: 8; right: clear.left; rightMargin: 8; verticalCenter: parent.verticalCenter }
        focus: true
        selectByMouse: true
    }

    Image {
        id: clear
        anchors { right: parent.right; rightMargin: 8; verticalCenter: parent.verticalCenter }
        source: "/home/evilbeast/skypefiles/返回.png"
        /* opacity: 0 */

        MouseArea { 
            anchors.fill: parent
            /* onClicked: { textInput.text = ''; focusScope.focus = true} */
            onClicked: focusScope.clicked()
        }
    }

    states: State {
        name: "hasText"; when: textInput.text != ''
        PropertyChanges { target: typeSomething; opacity: 0 }
        /* PropertyChanges { target: clear; opacity: 1 } */
    }

    transitions: [
        Transition {
            from: ""; to: "hasText"
            NumberAnimation { exclude: typeSomething; properties: "opacity" }
        },
        Transition {
            from: "hasText"; to: ""
            NumberAnimation { properties: "opacity" }
        }
    ]
}
