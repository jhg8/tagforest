import axios from 'axios'
import constants from '@/constants.js'

export default {
  parseStrList (s) {
    return s.split(',').map(x => x.trim().replace(/\s+/g, ' ')).filter(x => x);
  }
}
