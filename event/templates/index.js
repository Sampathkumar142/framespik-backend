// Set up WebSocket connection
const wsProtocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
const wsUrl = `${wsProtocol}${window.location.host}/ws/audio/`;
const ws = new WebSocket(wsUrl);

// Get mute button element
const muteButton = document.getElementById('muteButton');

// Set up audio stream
navigator.mediaDevices.getUserMedia({audio: true}).then(stream => {
  const audioContext = new AudioContext();
  const input = audioContext.createMediaStreamSource(stream);
  const processor = audioContext.createScriptProcessor(1024, 1, 1);
  const source = input.connect(processor);
  const destination = processor.connect(audioContext.destination);

  // Process audio data and send it to server via WebSocket
  processor.onaudioprocess = e => {
    if (!ws || ws.readyState !== WebSocket.OPEN) return;
    const inputData = e.inputBuffer.getChannelData(0);
    const outputData = new Float32Array(inputData.length);
    for (let i = 0; i < inputData.length; i++) {
      outputData[i] = inputData[i];
    }
    ws.send(outputData);
  };

  // Handle mute button clicks
  let isMuted = false;
  muteButton.addEventListener('click', () => {
    if (isMuted) {
      muteButton.innerHTML = '<i class="fa fa-microphone"></i>';
      processor.disconnect(audioContext.destination);
    } else {
      muteButton.innerHTML = '<i class="fa fa-microphone-slash"></i>';
      processor.connect(audioContext.destination);
    }
    isMuted = !isMuted;
  });
}).catch(err => {
  console.error(err);
  alert('Failed to get audio stream');
});

const audioContext = new AudioContext();
const gainNode = audioContext.createGain();
gainNode.connect(audioContext.destination);

let audioBuffer = null;

ws.binaryType = 'arraybuffer';

ws.onmessage = function(event) {
  const bytes = new Uint8Array(event.data);
  audioContext.decodeAudioData(bytes.buffer, function(buffer) {
    audioBuffer = buffer;
    const source = audioContext.createBufferSource();
    source.buffer = audioBuffer;
    source.connect(gainNode);
    source.start();
  });
};

function toggleMute() {
  gainNode.gain.value = gainNode.gain.value === 0 ? 1 : 0;
}