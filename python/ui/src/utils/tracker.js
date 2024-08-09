import ReactGA from 'react-ga';


const CATEGORY_MAP = {
  USER: 'user',
  EVENT: 'Event',
}


export default class Track {

  static user(action, label){
    ReactGA.event({
      category: CATEGORY_MAP.USER,
      action: action,
      label: label,
    });
  }

  static event(action, label){
    ReactGA.event({
      category: CATEGORY_MAP.EVENT,
      action: action,
      label: label,
    });
  }

  static exception(fatal, description){
    ReactGA.exception({
      description: description,
      fatal: fatal
    });
  }

}

