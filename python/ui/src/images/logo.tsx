// https://react-svgr.com/playground/?expandProps=start&typescript=true

import * as React from "react";
import { SVGProps } from "react";
const SvgComponent = (props: SVGProps<SVGSVGElement>) => (
  <svg
    {...props}
    xmlns="http://www.w3.org/2000/svg"
    // width={993.724}
    // height={624.828}
    viewBox="0 0 993.724 624.828"
  >
    <path
      fill="none"
      d="M0 0h993.724v624.828H0z"
      style={{
        fill: "#fff",
        fillOpacity: 0,
        pointerEvents: "none",
      }}
    />
    <path
      fill="currentColor"
      d="M804.04 243.094a186.032 186.032 0 0 0-36.884 3.688 152.105 152.105 0 0 0-80.291-105.741 152.098 152.098 0 0 0-132.744-2.406C515.856 33.233 399.39-21.187 293.99 17.078s-159.823 154.737-121.558 260.13C80.103 280.127 7.17 356.548 8.55 448.912c1.389 92.37 76.587 166.56 168.967 166.709H804.04c102.863 0 186.264-83.392 186.264-186.264 0-102.871-83.4-186.263-186.264-186.263zm0 0"
    />
  </svg>
);
export default SvgComponent;
