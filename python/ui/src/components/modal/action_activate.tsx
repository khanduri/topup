import React, { ChangeEventHandler, useState } from "react";

import SVGActivate from "images/icons/activate";
import SVGDeactivate from "images/icons/deactivate";

import { getStoredToken } from "utils/authentication";
import { BASE_URL } from "utils/xhr";
import LoadingSVG from "images/loading";

export default function Modal(props: any) {
  const { beneficiary, forceFetchCtr, setForceFetchCtr } = props;

  const [showModal, setShowModal] = React.useState(false);
  const [showError, setShowError] = useState(false);
  const [errorReason, setErrorReason] = useState("");
  const [balanceToAdd, setBalanceToAdd] = React.useState(0);

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setBalanceToAdd(parseInt(e.target.value || "0") || 0);
  };

  const [loadingActivate, setLoadingActivate] = useState(false);
  const onBeneficiaryActivate = async (
    beneficiary_xid: string,
    activate: boolean
  ) => {
    setShowError(false);
    try {
      setLoadingActivate(true);

      const body = {
        activate: activate,
      };
      const response = await fetch(
        BASE_URL + "/api/v1/topup/beneficiary/" + beneficiary_xid + "/activate",
        {
          method: "POST",
          headers: {
            Authorization: "Bearer " + getStoredToken(),
            "Content-Type": "application/json",
          },
          body: JSON.stringify(body),
        }
      );
      let response_data = await response.json();
      if (!response.ok) {
        throw new Error(`${response_data.data.message}`);
      }

      setForceFetchCtr(forceFetchCtr + 1);
    } catch (err: any) {
      setShowError(true);
      setErrorReason(err.message);
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
        {beneficiary.data.active ? (
          <div className="group flex relative text-red-600 hover:text-red-900">
            <span className="group-hover:opacity-100 transition-opacity bg-gray-500 px-1 text-sm text-gray-100 rounded-md absolute left-1/2 -translate-x-1/2 -translate-y-8 opacity-0 m-4 mx-auto">
              Deactivate
            </span>
            <span className="p-1">
              <SVGDeactivate className="w-6 h-6" />
            </span>
          </div>
        ) : (
          <div className="group flex relative rounded bg-indigo-100 text-indigo-600 hover:text-indigo-900">
            <span className="group-hover:opacity-100 transition-opacity bg-indigo-500 px-1 text-sm text-indigo-50 rounded-md absolute left-1/2 -translate-x-1/2 -translate-y-8 opacity-0 m-4 mx-auto">
              Activate user
            </span>
            <span className="p-1">
              <SVGActivate className="w-6 h-6" />
            </span>
          </div>
        )}
      </div>

      {showModal ? (
        <>
          <div className="font-normal justify-center items-center flex overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none">
            <div className="relative w-auto my-6 mx-auto max-w-3xl">
              <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
                {showError ? (
                  <div className=" border-red-400 rounded-b bg-red-100 px-4 py-3 text-red-700">
                    <p>Unable to Activate</p>
                    <p className="text-xs">{errorReason}</p>
                  </div>
                ) : (
                  ""
                )}
                <div className="flex items-start justify-between p-5 border-b border-solid  rounded-t">
                  <h3 className="text-3xl font-semibold">
                    {beneficiary.data.active
                      ? "Deactivate Beneficiary"
                      : "Activate Beneficiary"}
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
                  <div className="mb-4 ">
                    <div className="text-gray-400">Nickname</div>
                    <div className="text-xl text-gray-700">
                      {beneficiary.data.nickname}
                    </div>
                  </div>
                  <div className="mb-4 ">
                    <div className="text-gray-400">Email</div>
                    <div className="text-xl text-gray-700">
                      {beneficiary.data.email}
                    </div>
                  </div>

                  <div className={"pt-4 "}>
                    <button
                      className={
                        " text-white  py-2 px-4 rounded " +
                        (beneficiary.data.active
                          ? " bg-red-600 hover:bg-red-700 "
                          : " bg-green-600 hover:bg-green-700 ")
                      }
                      type="button"
                      onClick={() =>
                        onBeneficiaryActivate(
                          beneficiary.xid,
                          !beneficiary.data.active
                        )
                      }
                    >
                      {beneficiary.data.active ? "Deactivate" : "Activate"}
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
