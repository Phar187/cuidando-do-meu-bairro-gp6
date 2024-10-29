export function drawDonut (canvas, color, percentage) {
  var context = canvas.getContext('2d')
  var x = canvas.width / 2
  var y = canvas.height / 2
  var radius = 75
  var startAngle = 1.5 * Math.PI
  var endAngle = (1.5 + 2 * percentage / 100) * Math.PI
  var counterClockwise = false
  var whiteSpace = 0.01 * Math.PI
  var shadowStartAngle = endAngle + whiteSpace
  var shadowEndAngle = startAngle + 2 * Math.PI - whiteSpace

  var imageObj = new Image()
  imageObj.onload = function () {
    var pattern = context.createPattern(imageObj, 'repeat')
    context.strokeStyle = pattern

    context.clearRect(0, 0, canvas.width, canvas.height)
    context.beginPath()
    context.arc(x, y, radius, startAngle, endAngle, counterClockwise)
    context.lineWidth = 15

    context.stroke()

    if (shadowStartAngle < shadowEndAngle) {
      context.beginPath()
      context.arc(x, y, radius, shadowStartAngle, shadowEndAngle, counterClockwise)
      context.strokeStyle = 'lightgray'
      context.stroke()
    }
  }
  imageObj.src = color
}
