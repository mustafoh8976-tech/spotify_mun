(() => {
  const $ = (s) => document.querySelector(s);
  if (!$('#bar')) return;
  const audio = new Audio();
  const rows = [...document.querySelectorAll('.track[data-src]')];
  const els = {
    title: $('#bar-title'), hint: $('#bar-hint'), art: $('#bar-art'),
    toggle: $('#toggle'), prev: $('#prev'), next: $('#next'), all: $('#play-all'),
    seek: $('#seek'), cur: $('#cur'), dur: $('#dur'), vol: $('#vol'), mute: $('#mute'),
  };
  const PLAY = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>';
  const PAUSE = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 5h4v14H7zM13 5h4v14h-4z"/></svg>';
  const VOL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M11 5L6 9H2v6h4l5 4zM16 8a5 5 0 010 8"/></svg>';
  const MUTED = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5L6 9H2v6h4l5 4zM17 9l5 6M22 9l-5 6"/></svg>';
  let index = -1;

  const fmt = (t) => (isFinite(t) ? Math.floor(t / 60) + ':' + String(Math.floor(t % 60)).padStart(2, '0') : '0:00');
  const fill = (el) => el.style.setProperty('--p', (el.value / el.max) * 100 + '%');

  function paint() {
    const playing = !audio.paused;
    els.toggle.innerHTML = playing ? PAUSE : PLAY;
    els.toggle.setAttribute('aria-label', playing ? 'Пауза' : 'Играть');
    if (els.all) { els.all.innerHTML = playing ? PAUSE : PLAY; els.all.setAttribute('aria-label', playing ? 'Пауза' : 'Играть'); }
    rows.forEach((r, i) => {
      const on = i === index;
      r.classList.toggle('now', on);
      r.classList.toggle('playing', on && playing);
      r.querySelector('.play').innerHTML = on && playing ? PAUSE : PLAY;
    });
  }

  function load(i, autoplay = true) {
    if (!rows.length) return;
    index = (i + rows.length) % rows.length;
    const r = rows[index];
    audio.src = r.dataset.src;
    els.title.textContent = r.dataset.title;
    els.hint.textContent = 'Сейчас играет';
    els.art.style.setProperty('--h', r.dataset.hue);
    if (autoplay) audio.play().catch(() => {});
    paint();
  }

  function toggle() {
    if (index < 0) return load(0);
    audio.paused ? audio.play() : audio.pause();
  }

  rows.forEach((r, i) => {
    r.querySelector('.play').addEventListener('click', () => (i === index ? toggle() : load(i)));
    r.addEventListener('dblclick', () => load(i));
  });
  els.toggle.addEventListener('click', toggle);
  if (els.all) els.all.addEventListener('click', toggle);
  els.next.addEventListener('click', () => load(index + 1));
  els.prev.addEventListener('click', () => (audio.currentTime > 3 ? (audio.currentTime = 0) : load(index - 1)));
  audio.addEventListener('play', paint);
  audio.addEventListener('pause', paint);
  audio.addEventListener('ended', () => load(index + 1));
  audio.addEventListener('error', () => { els.hint.textContent = 'Не удалось воспроизвести файл'; paint(); });
  audio.addEventListener('loadedmetadata', () => { els.seek.max = audio.duration || 100; els.dur.textContent = fmt(audio.duration); });
  audio.addEventListener('timeupdate', () => { els.seek.value = audio.currentTime; els.cur.textContent = fmt(audio.currentTime); fill(els.seek); });
  els.seek.addEventListener('input', () => { audio.currentTime = els.seek.value; fill(els.seek); });
  els.vol.addEventListener('input', () => { audio.muted = false; audio.volume = els.vol.value; els.mute.innerHTML = +els.vol.value ? VOL : MUTED; fill(els.vol); });
  els.mute.addEventListener('click', () => {
    audio.muted = !audio.muted;
    els.mute.innerHTML = audio.muted ? MUTED : VOL;
    els.vol.value = audio.muted ? 0 : audio.volume; fill(els.vol);
  });
  fill(els.vol);

  document.addEventListener('keydown', (e) => {
    if (e.code === 'Space' && !/INPUT|TEXTAREA|BUTTON|A/.test(e.target.tagName)) { e.preventDefault(); toggle(); }
  });
  document.querySelectorAll('[data-confirm]').forEach((el) =>
    el.addEventListener(el.tagName === 'FORM' ? 'submit' : 'click', (e) => { if (!confirm(el.dataset.confirm)) e.preventDefault(); }));
})();
