import QtQuick 2.1
import QtGraphicalEffects 1.0


Item {
    
    id: root
    
    width: content.width
    height: content.height
    property string text: "LinuxDeepin"    
    property alias clip: content.clip
    property alias color: content.color
    property alias contentWidth: content.contentWidth
    property alias contentHeight: content.contentHeight
    property alias font: content.font
    property alias horizontalAlignment: content.horizontalAlignment
    property alias verticalAlignment: content.verticalAlignment
    property alias renderType: content.renderType
    property alias textFormat: content.textFormat
    property alias truncated: content.truncated
    property alias wrapMode: content.wrapMode
    
    Text{
        id: content
        text: " " + root.text + " "
        color: "#fff"
        font.pixelSize: 12
        height: implicitHeight + glow.radius * 2
        verticalAlignment: Text.AlignVCenter
    }
    
    Glow{
        id: glow
        source: ShaderEffectSource{sourceItem: content; hideSource: true}
        anchors.fill: content
        radius: 5
        samples: 16
        color: "#000"
    }
}
