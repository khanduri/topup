import { useState } from "react";
import { useOutsideClick } from "components/hooks/useOutsideClick";

// {/* <!-- Settings panel --> */}
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

  return (
    <div
      ref={refSettingPanel}
      // x-show="isOpen"
      // @click.away="isOpen = false"
      // x-transition:enter="transition transform duration-300"
      // x-transition:enter-start="translate-x-full opacity-30  ease-in"
      // x-transition:enter-end="translate-x-0 opacity-100 ease-out"
      // x-transition:leave="transition transform duration-300"
      // x-transition:leave-start="translate-x-0 opacity-100 ease-out"
      // x-transition:leave-end="translate-x-full opacity-0 ease-in"
      // style="backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px)"
      className={
        "fixed inset-y-0 right-0 flex flex-col bg-white shadow-lg bg-opacity-95 w-80 " +
        (isOpen ? " " : " hidden ")
      }
    >
      <div className="flex items-center justify-between flex-shrink-0 p-2">
        <h6 className="p-2 text-lg">Settings</h6>
        <button
          // @click="isOpen = false"
          onClick={() => setIsOpen(false)}
          className="p-2 rounded-md focus:outline-none focus:ring"
        >
          <svg
            className="w-6 h-6 text-gray-600"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      </div>
      <div className="flex-1 max-h-full p-4 overflow-hidden hover:overflow-y-scroll">
        <span>Settings Content</span>
        {/* <!-- Settings Panel Content ... --> */}
      </div>
    </div>
  );
}
