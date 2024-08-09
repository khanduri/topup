import { useState } from "react";

import PanelProfile from "components/panel_profile";
import PanelOptions from "components/panel_options";

export default function Component({
  isSidebarOpen,
  setIsSidebarOpen,
}: {
  isSidebarOpen: boolean;
  setIsSidebarOpen: any;
}) {
  const [isProfilePanelOpen, setIsProfilePanelOpen] = useState(false);
  const [isNotificationPanelOpen, setIsNotificationPanelOpen] = useState(false);

  return (
    <>
      {/* <!-- Navbar --> */}
      <header className="flex-shrink-0 border-b">
        <div className="flex items-center justify-between p-2">
          {/* <!-- Navbar left --> */}
          <div className="flex items-center space-x-3">
            <span className="p-2 text-xl font-semibold tracking-wider lg:hidden">
              TopUp
            </span>
            {/* <!-- Toggle sidebar button --> */}
            <button
              // @click="toggleSidbarMenu()"
              onClick={() => setIsSidebarOpen(!isSidebarOpen)}
              className="p-2 rounded-md focus:outline-none focus:ring"
            >
              <svg
                className={
                  "w-4 h-4 text-gray-600 " +
                  (isSidebarOpen
                    ? " transform transition-transform -rotate-180  "
                    : " ")
                }
                // :className="{'transform transition-transform -rotate-180': isSidebarOpen}"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth="2"
                  d="M13 5l7 7-7 7M5 5l7 7-7 7"
                />
              </svg>
            </button>
          </div>

          {/* <!-- Navbar right --> */}
          <div className="relative flex items-center space-x-3">
            {/* <!-- Profile button --> */}
            <div className="relative">
              <button
                onClick={() => setIsProfilePanelOpen(true)}
                className="p-1 bg-gray-200 rounded-full focus:outline-none focus:ring"
              >
                <span className="object-cover w-8 h-8 rounded-full">
                  <svg
                    className="w-6 h-6 text-gray-500"
                    viewBox="0 0 24 24"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <circle
                      cx="12"
                      cy="6"
                      r="4"
                      stroke="currentColor"
                      strokeWidth="1.5"
                    />
                    <path
                      d="M15 20.6151C14.0907 20.8619 13.0736 21 12 21C8.13401 21 5 19.2091 5 17C5 14.7909 8.13401 13 12 13C15.866 13 19 14.7909 19 17C19 17.3453 18.9234 17.6804 18.7795 18"
                      stroke="currentColor"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                    />
                  </svg>
                </span>
              </button>
              <div className="absolute right-0 p-1 bg-green-400 rounded-full bottom-3 animate-ping"></div>
              <div className="absolute right-0 p-1 bg-green-400 border border-white rounded-full bottom-3"></div>
              <PanelProfile
                isOpen={isProfilePanelOpen}
                setIsOpen={setIsProfilePanelOpen}
              />
            </div>
          </div>
        </div>
      </header>
    </>
  );
}
