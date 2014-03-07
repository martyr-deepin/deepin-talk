import QtQuick 2.1

Item {
	id: titlebar
	
    signal closed
    signal minimized
    signal maximized
    signal menued
    
    property int menu: 1 << 2
    property int min: 1 << 3
    property int max: 1 << 4
    property int close: 1 << 5
    
    property int buttons: menu | min | max | close
    
    property Component leftItem
    
	function getImage (name) {
		return "qrc:/images/button/" + name + ".png"
	}
    
    Loader {
        id: leftLoader 
        sourceComponent: leftItem
        anchors.left: parent.left
        /* anchors.verticalCenter: parent.verticalCenter */
    }
	
	Row {
		id : control
		
		anchors.right: parent.right
		anchors.rightMargin: 5
        /* anchors.verticalCenter: parent.verticalCenter */
				
		ImageButton {
			normalImage: getImage("window_menu_normal")
			hoverImage: getImage("window_menu_hover")
			pressImage: getImage("window_menu_press")
            visible: buttons & menu
            onClicked: menued()
		}
		
		ImageButton {
			normalImage: getImage("window_min_normal")
			hoverImage: getImage("window_min_hover")
			pressImage: getImage("window_min_press")
            onClicked: { windowView.doMinimized(); minimized() }
            visible: buttons & min
		}
		
		ImageButton {
			normalImage: getImage("window_max_normal")
			hoverImage: getImage("window_max_hover")
			pressImage: getImage("window_max_press")
            onClicked: maximized()
            visible: buttons & max
		}
		
		ImageButton {
			normalImage: getImage("window_close_normal")
			hoverImage: getImage("window_close_hover")
			pressImage: getImage("window_close_press")
            onClicked: {
                titlebar.closed()
            }
            visible: buttons & close
		}
		
	}
	
}