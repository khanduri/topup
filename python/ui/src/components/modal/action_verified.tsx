import React, { ChangeEventHandler, useState } from "react";

import SVGActivate from "images/icons/activate";
import SVGDeactivate from "images/icons/deactivate";

import { getStoredToken } from "utils/authentication";
import { BASE_URL } from "utils/xhr";
import LoadingSVG from "images/loading";

export default function Modal(props: any) {
  const { verified, forceFetchCtr, setForceFetchCtr } = props;

  const [showModal, setShowModal] = React.useState(false);
  const [balanceToAdd, setBalanceToAdd] = React.useState(0);

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setBalanceToAdd(parseInt(e.target.value || "0") || 0);
  };

  const [loadingActivate, setLoadingActivate] = useState(false);
  const onUserVerification = async (verified: boolean) => {
    try {
      setLoadingActivate(true);

      const body = {
        action: "VERIFY_USER",
        action_data: verified,
      };
      const response = await fetch(BASE_URL + "/api/v1/topup/users", {
        method: "POST",
        headers: {
          Authorization: "Bearer " + getStoredToken(),
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });
      if (!response.ok) {
        throw new Error(`HTTP error: Status ${response.status}`);
      }
      let response_data = await response.json();

      setForceFetchCtr(forceFetchCtr + 1);
    } catch (err) {
    } finally {
      setLoadingActivate(false);
    }
  };
  const freq_add = [10, 20, 30, 50, 75, 100];

  return (
    <>
      <div
        className="cursor-pointer text-indigo-600 hover:text-indigo-900 group flex relative"
        onClick={() => setShowModal(true)}
      >
        {verified ? (
          <span className=" bg-green-500 text-green-50 py-1 px-2 text-xs rounded ml-1">
            verified
          </span>
        ) : (
          <span className=" bg-red-500 text-red-50 py-1 px-2 text-xs rounded ml-1">
            unverified
          </span>
        )}
      </div>

      {showModal ? (
        <>
          <div className="font-normal justify-center items-center flex overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none">
            <div className="relative w-auto my-6 mx-auto max-w-3xl">
              <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
                <div className="flex items-start justify-between p-5 border-b border-solid  rounded-t">
                  <h3 className="text-3xl font-semibold">
                    {verified ? "Unverify User" : "Verify User"}
                  </h3>
                  <button
                    className="p-1 ml-auto bg-transparent border-0 text-black opacity-5 float-right text-3xl leading-none font-semibold outline-none focus:outline-none"
                    onClick={() => setShowModal(false)}
                  >
                    <span className="bg-transparent text-black opacity-5 h-6 w-6 text-2xl block outline-none focus:outline-none">
                      ×
                    </span>
                  </button>
                </div>

                <div className="relative p-6 flex-auto">
                  <div className={"pt-4 "}>
                    <button
                      className={
                        " text-white  py-2 px-4 rounded " +
                        (verified
                          ? " bg-red-600 hover:bg-red-700 "
                          : " bg-green-600 hover:bg-green-700 ")
                      }
                      type="button"
                      onClick={() => onUserVerification(!verified)}
                    >
                      {verified ? "Unverify" : "Verify"}
                    </button>
                  </div>
                </div>

                <div className="flex items-center justify-end p-6 border-t border-solid border-blueGray-200 rounded-b">
                  <button
                    className="text-red-500 background-transparent font-bold uppercase px-6 py-2 text-sm outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150"
                    type="button"
                    onClick={() => setShowModal(false)}
                  >
                    Close
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div className="opacity-25 fixed inset-0 z-40 bg-black"></div>
        </>
      ) : null}
    </>
  );
}
