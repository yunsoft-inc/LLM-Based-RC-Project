// 1. Firebase 설정 (아래 config는 본인 프로젝트로 교체)
const firebaseConfig = {
  apiKey: "",
  authDomain: "",
  databaseURL: "",
  projectId: "",
  storageBucket: "",
  messagingSenderId: "",
  appId: ""
};
firebase.initializeApp(firebaseConfig);
const db = firebase.database().ref('com/entry');

// 상태 변수
let prevLog = '';
let logLines = [];
let prevDepth = '';
let prevRgb = '';
let logMaxLines = 100;
let logTimestamps = [];
let lastUpdate = '';
let onlineStatus = false;

// 실시간 리스너
db.on('value', (snap) => {
  const data = snap.val();
  if (!data) return;

  // Bootloader
  document.getElementById('bootloaderSwitch').checked = data.bootloader === 1;
  document.getElementById('bootloaderStatus').textContent = data.bootloader === 1 ? '참' : '거짓';

  // Start 상태
  document.getElementById('startStatus').textContent = getStartStatus(data.start);

  // 이미지
  if (data.image_update === 1) {
    prevDepth = data.depth;
    prevRgb = data.rgb;
    db.child('image_update').set(0);
  }
  document.getElementById('depthImg').src = prevDepth || data.depth || '';
  document.getElementById('rgbImg').src = prevRgb || data.rgb || '';

  // 로그 (시간과 함께, 최대 logMaxLines 유지)
  if (data.log !== prevLog) {
    const now = new Date();
    const timeStr = now.toLocaleTimeString();
    logLines.push(`[${timeStr}] ${data.log}`);
    logTimestamps.push(now);
    prevLog = data.log;
    if (logLines.length > logMaxLines) {
      logLines.shift();
      logTimestamps.shift();
    }
  }
  updateLogBox();

  // 프롬프트 (textarea)
  const promptInput = document.getElementById('promptInput');
  if (!promptInput.value) promptInput.value = data.prompt || '';

  // prompt_change 처리
  if (data.prompt_change === 2) {
    db.child('prompt_change').set(0);
  }

  // 업데이트 시간
  document.getElementById('updateTime').textContent = data.update || '';
  lastUpdate = data.update || '';
  updateOnlineStatus();
});

// Bootloader 토글
document.getElementById('bootloaderSwitch').addEventListener('change', function() {
  db.child('bootloader').set(this.checked ? 1 : 0);
});

// Start 제어
function setStart(val) {
  db.child('start').set(val);
}

// 프롬프트 수정
function updatePrompt() {
  const val = document.getElementById('promptInput').value;
  db.child('prompt').set(val);
  db.child('prompt_change').set(1);
}

// 로그 업데이트 및 스크롤
function updateLogBox() {
  const logBox = document.getElementById('logBox');
  logBox.textContent = logLines.join('\n');
  // 자동 스크롤
  const container = document.getElementById('logBoxContainer');
  container.scrollTop = container.scrollHeight;
}

// 로그 초기화
function clearLog() {
  logLines = [];
  logTimestamps = [];
  prevLog = '';
  updateLogBox();
}

// 상태 변환 함수
function getStartStatus(val) {
  switch(val) {
    case -1: return '장비 종료';
    case 0: return '부트로더 모드';
    case 1: return '서비스 시작';
    case 2: return '서비스 실행중';
    default: return '알 수 없음';
  }
}

// 온라인/오프라인 상태 갱신
function updateOnlineStatus() {
  const statusElem = document.getElementById('onlineStatus');
  onlineStatus = isOnline(lastUpdate);
  statusElem.textContent = onlineStatus ? '온라인' : '오프라인';
  statusElem.style.color = onlineStatus ? 'green' : 'red';
}
function isOnline(update) {
  if (!update) return false;
  try {
    const last = new Date(update.replace(' ', 'T'));
    return Math.abs(Date.now() - last.getTime()) < 10000;
  } catch { return false; }
}
// 5초마다 온라인 상태 갱신
setInterval(updateOnlineStatus, 5000);

// 명시적으로 전역 등록
window.clearLog = clearLog;
window.setStart = setStart;
window.updatePrompt = updatePrompt; 