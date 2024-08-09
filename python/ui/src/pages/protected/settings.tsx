import { useState } from "react";

import SidenavLayout from "pages/layout/sidenav";
import Title from "components/convention/title";

export default function Page() {
  return (
    <SidenavLayout>
      <Title type="sidenav-page">Settings</Title>
      <div className="my-4 ">Coming soon ... </div>
    </SidenavLayout>
  );
}
