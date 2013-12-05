import QtQuick 2.0

Item {
	id: titlebar
	
	function get_image (name) {
		return "image/button/" + name + ".png"
	}
	
	Row {
		id : control
		
		anchors.right: parent.right
		anchors.rightMargin: 5
				
		ImageButton {
			normal_image: get_image("window_menu_normal")
			hover_image: get_image("window_menu_hover")
			press_image: get_image("window_menu_press")
		}
		
		ImageButton {
			normal_image: get_image("window_min_normal")
			hover_image: get_image("window_min_hover")
			press_image: get_image("window_min_press")
		}
		
		ImageButton {
			normal_image: get_image("window_max_normal")
			hover_image: get_image("window_max_hover")
			press_image: get_image("window_max_press")
		}
		
		ImageButton {
			normal_image: get_image("window_close_normal")
			hover_image: get_image("window_close_hover")
			press_image: get_image("window_close_press")
		}
		
	}
	
}