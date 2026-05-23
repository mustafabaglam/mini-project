const fs = require('fs')
const path = require('path')
const http = require('http')
const { Server } = require('socket.io')
const { SerialPort } = require('serialport')

const PORT = 3000
const SERIAL_PATH = '/dev/ttyACM0' // Linux: /dev/ttyUSB0 veya /dev/ttyACM0 | macOS: /dev/tty.usbmodem... | Windows: COM3

const server = http.createServer((req, res) => {
  let filePath = req.url === '/' ? '/index.html' : req.url
  filePath = path.join(__dirname, 'public', filePath)

  const ext = path.extname(filePath)
  const contentTypes = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css' }
  const contentType = contentTypes[ext] || 'text/plain'

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(err.code === 'ENOENT' ? 404 : 500)
      res.end()
      return
    }
    res.writeHead(200, { 'Content-Type': contentType })
    res.end(data)
  })
})

const io = new Server(server)

const sp = new SerialPort({ path: SERIAL_PATH, baudRate: 9600 })

sp.on('open', () => console.log('Arduino bağlandı.'))
sp.on('close', () => console.log('Seri port kapatıldı.'))
sp.on('error', (err) => console.error('Seri port hatası:', err.message))

let buffer = ''
sp.on('data', (data) => {
  buffer += data.toString()
  const lines = buffer.split('\n')
  buffer = lines.pop() // son yarım satırı sakla
  for (const line of lines) {
    const trimmed = line.trim()
    if (!trimmed) continue
    try {
      JSON.parse(trimmed) // geçerli JSON kontrolü
      console.log('gönderiliyor:', trimmed)
      io.emit('message', trimmed)
    } catch (e) {
      console.warn('geçersiz veri:', trimmed)
    }
  }
})

io.on('connection', (socket) => {
  console.log('Tarayıcı bağlandı')
  socket.on('disconnect', () => console.log('Tarayıcı ayrıldı'))
})

server.listen(PORT, () => console.log(`Sunucu çalışıyor: http://localhost:${PORT}`))
