import QtQuick 2.1
import QtQuick.Window 2.1
import "../Widgets"

Item {
	width: status.width + down.width + statusRow.spacing
	height: Math.max(status.height, down.height)
	
	Row {
		id: statusRow
		anchors.fill: parent
		spacing: 5		
		
		Image {
			id: status
			source: "qrc:/images/status/online.png"
			anchors.verticalCenter: parent.verticalCenter
		}
		Image {
			id: down
			source: "qrc:/images/status/status_arrow_down.png"
			anchors.verticalCenter: parent.verticalCenter
		}
	
	}
	
	MouseArea {
		anchors.fill: parent
		hoverEnabled: true
		onClicked: {
			var pos = parent.mapToItem(null, parent.x, parent.y + parent.height)
			var target_x = windowView.x + pos.x
			var target_y = windowView.y + pos.y
			statusWindow.x = target_x
			statusWindow.y = target_y
			statusWindow.visible = true
		}
	}
	
	ListModel {
		id: statusModel
		ListElement { type: 0; icon: "qrc:/images/status/online.png"; label: "在线" }
		ListElement { type: 1; icon: "qrc:/images/status/hide.png"; label: "隐身" }
		ListElement { type: 2; icon: "qrc:/images/status/busy.png"; label: "忙碌" }
		ListElement { type: 3; icon: "qrc:/images/status/leave.png"; label: "离开" }
	}
	
	Component {
		id: statusDelegate
		
		Item {
			id: wrapper
			width: ListView.view.width; height: 22
			Row {
				spacing: 10
				anchors.margins: 12
				anchors.fill: parent
				Image {
					id: statusIcon
					source: model.icon
					anchors.verticalCenter: parent.verticalCenter
				}
				Text {
					id: statusLabel
					text: model.label
					anchors.verticalCenter: parent.verticalCenter
					/* color: wrapper.ListView.isCurrentItem ? "#fff" : Qt.rgba(0.1, 0.1, 0.1, 0.8) */
					color: Qt.rgba(0.1, 0.1, 0.1, 0.8)
				}
			}
			
			MouseArea {
				id: statusMouseArea
				hoverEnabled: true
				anchors.fill: parent
				onEntered: {
					wrapper.ListView.view.currentIndex = index
				}
				
				onClicked: {
					status.source = model.icon
					statusWindow.visible = false
				}
			}
			
		}	
	}
	
	PopupWindow {
		id: statusWindow
		width: 86; height: 110
		visible: false
		Rectangle {
			anchors.fill: parent
			anchors.margins: 2
			color: "transparent"
			ListView {
				anchors.topMargin: 10
				id: statusView
				anchors.fill: parent
				model: statusModel
				delegate: statusDelegate
				interactive: false
				highlight: Rectangle {
					color: "#7A65B8"
				}
				focus: true
			}
		}
	}
	
} 