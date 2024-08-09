import { useState } from "react";

import SideBar from "components/sidebar";

import HeaderSection from "components/header";
import FooterSection from "components/footer";

// import PanelSetting from "components/panel_settings";

export default function Page(props: any) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  //   const [isSettingsPanelOpen, setIsSettingsPanelOpen] = useState(false);

  return (
    <div>
      <div className="flex h-screen overflow-y-hidden bg-white">
        <SideBar isOpen={isSidebarOpen} setIsOpen={setIsSidebarOpen} />

        <div className="flex flex-col flex-1 h-full overflow-hidden">
          <HeaderSection
            isSidebarOpen={isSidebarOpen}
            setIsSidebarOpen={setIsSidebarOpen}
          />

          <main className="flex-1 max-h-full p-5 overflow-hidden overflow-y-scroll">
            {props.children}
          </main>

          <FooterSection />
        </div>

        {/* <!-- Setting panel button --> */}
        {/* <button
          onClick={() => setIsSettingsPanelOpen(true)}
          className="fixed right-0 px-4 py-2 text-sm font-medium text-white uppercase transform rotate-90 translate-x-8 bg-gray-600 top-1/2 rounded-b-md"
        >
          Settings
        </button>
        <PanelSetting
          isOpen={isSettingsPanelOpen}
          setIsOpen={setIsSettingsPanelOpen}
        /> */}
      </div>
    </div>
  );
}
