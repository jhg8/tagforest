export default {
  parseStrList (s) {
    return s.split(',').map(x => x.trim().replace(/\s+/g, ' ')).filter(x => x);
  }
}
