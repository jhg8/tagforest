import axios from 'axios'
import constants from '@/constants.js'

export default {
  parseStrList (s) {
    const list = s.split(',').map(x => x.trim().replace(/\s+/g, ' ')).filter(x => x);
    const parsed_list = [];
    for(const x of list) {
      let tag_category = x.split(';');
      let tag = tag_category.at(0);
      let category = tag_category.at(1);
      if(tag && category) {
        parsed_list.push({'tag': tag, 'category': category});
      }
    }
    return parsed_list;
  }
}
