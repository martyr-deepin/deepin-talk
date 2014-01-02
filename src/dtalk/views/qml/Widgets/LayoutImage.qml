import QtQuick 2.1
 
Image {
    id: sourceImage
 
    property real minWidth: 0
    property real maxWidth: 10000
 
    property real minHeight: 0
    property real maxHeight: 10000
 
    property real dynamicWidth: 0
    property real dynamicHeight: 0
 
 
    function updateWidth(){
 
        dynamicWidth = widthComputingWorkaround.width
 
        if( dynamicWidth > maxWidth ){
            dynamicWidth = maxWidth
        }
        if( dynamicWidth < minWidth ){
            dynamicWidth = minWidth
        }
        if( dynamicWidth < 0 ){
            dynamicWidth = 0
        }
 
        dynamicHeight = widthComputingWorkaround.width
 
        if( dynamicHeight > maxHeight ){
            dynamicHeight = maxHeight
        }
        if( dynamicHeight < minHeight ){
            dynamicHeight = minHeight
        }
        if( dynamicHeight < 0 ){
            dynamicHeight = 0
        }
    }
 
    width: dynamicWidth
    height: dynamicHeight
 
    Image {
        id: widthComputingWorkaround
        source: source.source
        opacity: 0
        onSourceChanged: updateWidth()
    }
 
    onMinWidthChanged: updateWidth()
    onMaxWidthChanged: updateWidth()
    onMinHeightChanged: updateWidth()
    onMaxHeightChanged: updateWidth()
    Component.onCompleted: updateWidth()
}