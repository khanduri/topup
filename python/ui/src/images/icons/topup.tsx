// https://react-svgr.com/playground/?expandProps=start&typescript=true

import * as React from "react";
import { SVGProps } from "react";
const SvgComponent = (props: SVGProps<SVGSVGElement>) => (
  <svg
    {...props}
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
  >
    <circle cx="12" cy="6" r="4" stroke="currentColor" strokeWidth="1.5" />
    <path
      d="M20.4141 18.5H18.9999M18.9999 18.5H17.5857M18.9999 18.5L18.9999 17.0858M18.9999 18.5L18.9999 19.9142"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
    />
    <path
      d="M12 13C14.6083 13 16.8834 13.8152 18.0877 15.024M15.5841 20.4366C14.5358 20.7944 13.3099 21 12 21C8.13401 21 5 19.2091 5 17C5 15.6407 6.18652 14.4398 8 13.717"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
    />
  </svg>
);
export default SvgComponent;
