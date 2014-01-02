import QtQuick 2.1

Item {
    id: container
 
    property variant scrollArea
	property real visibleSize: 8
    property variant orientation: Qt.Vertical
	property bool traditional: true
	property bool drawBackground: true
	
	Component.onCompleted: {
		layout()
	}
	
    opacity: 0
	
	function layout() {
		if (container.orientation == Qt.Vertical){
			container.anchors.top = scrollArea.top
			container.anchors.bottom = scrollArea.bottom
			container.anchors.right = scrollArea.right
			container.height = scrollArea.height
			container.width = container.visibleSize
			
		} else {
			container.anchors.left = scrollArea.left
			container.anchors.right = scrollArea.right
			container.anchors.bottom = scrollArea.bottom
			container.height = container.visibleSize
			container.width = scrollArea.width
		}
	}
 
    function position()
    {
        var ny = 0;
        if (container.orientation == Qt.Vertical)
            ny = scrollArea.visibleArea.yPosition * container.height;
        else
            ny = scrollArea.visibleArea.xPosition * container.width;
        if (ny > 2) return ny; else return 2;
    }
 
    function size()
    {
        var nh, ny;
 
        if (container.orientation == Qt.Vertical)
            nh = scrollArea.visibleArea.heightRatio * container.height;
        else
            nh = scrollArea.visibleArea.widthRatio * container.width;
 
        if (container.orientation == Qt.Vertical)
            ny = scrollArea.visibleArea.yPosition * container.height;
        else
            ny = scrollArea.visibleArea.xPosition * container.width;
 
        if (ny > 3) {
            var t;
            if (container.orientation == Qt.Vertical)
                t = Math.ceil(container.height - 3 - ny);
            else
                t = Math.ceil(container.width - 3 - ny);
            if (nh > t) return t; else return nh;
        } else return nh + ny;
    }
	
	function fire() {
		if (container.orientation == Qt.Vertical) {
			if (container.traditional)
			    return scrollArea.contentHeight > scrollArea.height
			else	
			    return scrollArea.movingVertically
		} else {
			if (container.traditional)
			    return scrollArea.contentWidth > scrollArea.width
			else	
			    return scrollArea.movingHorizontally
		}
	}
 
    Rectangle { 
		anchors.fill: parent; 
		color: "white"; 
		opacity: 0.3; radius:5; smooth: true
		visible: container.drawBackground
	}
 
    Rectangle {
		id: scrollBorder
		radius: 3; opacity: 0.7; color: "black"
        x: 2; width: container.width - 4; y: 2; height: container.height - 4
		visible: scrollArea.contentHeight > scrollArea.height || scrollArea.contentWidth > scrollArea.width && container.traditional
		MouseArea {
			id: mouseArea
			anchors.fill: parent
			drag.target: parent
			drag.axis: container.orientation == Qt.Vertical ? Drag.YAxis : Drag.XAxis
			drag.minimumX: container.x
			drag.maximumX: container.width - parent.width
			drag.minimumY: container.y
			drag.maximumY: container.height - parent.height
			
			onPositionChanged: {
				if (container.orientation == Qt.Vertical)
				    scrollArea.contentY = (parent.y / container.height) * scrollArea.contentHeight
				else	
				    scrollArea.contentX = (parent.x / container.width) * scrollArea.contentWidth
			}
		}
		
		Binding { 
			target: scrollBorder; property: "x"; value: position()
			when: !mouseArea.pressed && container.orientation != Qt.Vertical
		}
		Binding { 
			target: scrollBorder; property: "y"; value: position()
			when: !mouseArea.pressed && container.orientation == Qt.Vertical
		}
		Binding { 
			target: scrollBorder; property: "width"; value: size()
			when: !mouseArea.pressed && container.orientation != Qt.Vertical
		}
		Binding { 
			target: scrollBorder; property: "height"; value: size()
			when: !mouseArea.pressed && container.orientation == Qt.Vertical
		}
    }
 
    states: State {
        name: "visible"

        when: fire()
        PropertyChanges { target: container; opacity: 1.0 }
    }
 
    transitions: Transition {
        from: "visible"; to: ""
        NumberAnimation { properties: "opacity"; duration: 600 }
    }
}