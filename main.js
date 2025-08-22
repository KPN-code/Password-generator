const els = {
  length: document.getElementById('length'),
  lenLabel: document.getElementById('lenLabel'),
  lower: document.getElementById('lower'),
  upper: document.getElementById('upper'),
  digits: document.getElementById('digits'),
  symbols: document.getElementById('symbols'),
  avoid: document.getElementById('avoid'),
  generate: document.getElementById('generate'),
  password: document.getElementById('password'),
  copy: document.getElementById('copy'),
  bar: document.getElementById('bar'),
  strengthLabel: document.getElementById('strengthLabel'),
};

els.lenLabel.textContent = els.length.value;
els.length.addEventListener('input', () => (els.lenLabel.textContent = els.length.value));

function zxcvbnLite(pwd) {
  // Simple, dependency-free strength heuristic
  let score = 0;
  if (!pwd) return 0;
  const sets = [/[a-z]/, /[A-Z]/, /[0-9]/, /[!@#$%^&*\-_=+?]/];
  score += Math.min(4, sets.reduce((acc, re) => acc + (re.test(pwd) ? 1 : 0), 0));
  score += Math.min(4, Math.floor(pwd.length / 4)); // length contribution
  // Penalize repeats
  const repeats = /(.)\1{2,}/.test(pwd) ? 1 : 0;
  score -= repeats;
  return Math.max(0, Math.min(8, score));
}

function renderStrength(score) {
  const pct = (score / 8) * 100;
  els.bar.style.width = pct + '%';
  const labels = ['Very weak', 'Weak', 'Okay', 'Fair', 'Good', 'Strong', 'Very strong', 'Excellent', 'Elite'];
  els.strengthLabel.textContent = labels[Math.round(score)] || '—';
}

async function generate() {
  const payload = {
    length: Number(els.length.value),
    lower: els.lower.checked,
    upper: els.upper.checked,
    digits: els.digits.checked,
    symbols: els.symbols.checked,
    avoidAmbiguous: els.avoid.checked,
  };

  const res = await fetch('/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  const data = await res.json();
  if (data.error) {
    alert(data.error);
    return;
  }
  els.password.value = data.password;
  renderStrength(zxcvbnLite(data.password));
}

els.generate.addEventListener('click', generate);
els.copy.addEventListener('click', async () => {
  if (!els.password.value) return;
  try {
    await navigator.clipboard.writeText(els.password.value);
    els.copy.textContent = 'Copied!';
    setTimeout(() => (els.copy.textContent = 'Copy'), 1200);
  } catch (_) {
    // Fallback
    els.password.select();
    document.execCommand('copy');
  }
});
