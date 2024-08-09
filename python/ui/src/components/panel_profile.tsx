import { useState } from "react";
import { useOutsideClick } from "components/hooks/useOutsideClick";
import { useAuth } from "./hooks/useAuth";

// {/* <!-- Dropdown card --> */}
export default function Component({
  isOpen,
  setIsOpen,
}: {
  isOpen: boolean;
  setIsOpen: any;
}) {
  const refSettingPanel = useOutsideClick(() => {
    setIsOpen(false);
  });

  const { logout } = useAuth();
  return (
    <div
      ref={refSettingPanel}
      className={
        "absolute mt-3 transform -translate-x-full bg-white rounded-md shadow-lg min-w-max " +
        (isOpen ? " " : " hidden ")
      }
    >
      <div className="flex flex-col p-4 space-y-1 font-medium border-b">
        <span className="text-gray-800">Prashant Khanduri</span>
        <span className="text-sm text-gray-400">prashant.khanduri@gmail.com</span>
      </div>
      <ul className="flex flex-col p-2 my-2 space-y-1">
        <li>
          <a
            href="#"
            className="block px-2 py-1 transition rounded-md hover:bg-gray-100"
          >
            TopUp Home
          </a>
        </li>
      </ul>
      <div className="flex items-center justify-center p-4 text-blue-700 underline border-t">
        <a href="#" onClick={logout}> Logout</a>
      </div>
    </div>
  );
}
