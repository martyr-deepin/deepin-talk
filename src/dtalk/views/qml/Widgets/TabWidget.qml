import QtQuick 2.1

Item {
    id: tabWidget

    // Setting the default property to stack.children means any child items
    // of the TabWidget are actually added to the 'stack' item's children.
    // See the "Property Binding"
    // documentation for details on default properties.
    default property alias content: stack.children

    property int current: 0

    onCurrentChanged: setVisibles()
    Component.onCompleted: setVisibles()

	
	function getTabImage(name) {
		return "qrc:/images/" + name + ".png"
	}

    function setVisibles() {
        for (var i = 0; i < stack.children.length; ++i) {
            stack.children[i].visible = (i == current ? true : false)
        }
    }

    Row {
        id: header

        Repeater {
            model: stack.children.length
            delegate: Item {
                width: tabWidget.width / stack.children.length; height: 40

				Rectangle {
					anchors.fill: parent
					id: tabBack
					color: tabWidget.current == index ? "transparent" : Qt.rgba(0.9, 0.9, 0.9, 0.3)
				}
				
				Image {
					source: getTabImage(stack.children[index].title)
					anchors.centerIn: parent           
				}

                MouseArea {
                    anchors.fill: parent
                    onClicked: tabWidget.current = index
                }
            }
        }
    }

    Item {
        id: stack
        width: tabWidget.width
        anchors.top: header.bottom; anchors.bottom: tabWidget.bottom
    }
}
