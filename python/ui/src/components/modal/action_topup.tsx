import React, { ChangeEventHandler, useState } from "react";

import { getStoredToken } from "utils/authentication";
import { BASE_URL } from "utils/xhr";
import LoadingSVG from "images/loading";
import SVGTopUp from "images/icons/topup";

export default function Modal(props: any) {
  const { beneficiary, forceFetchCtr, setForceFetchCtr } = props;

  const [showModal, setShowModal] = useState(false);
  const [showError, setShowError] = useState(false);
  const [errorReason, setErrorReason] = useState("");
  const [balanceToAdd, setBalanceToAdd] = useState(0);

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setBalanceToAdd(parseInt(e.target.value || "0") || 0);
    setShowError(false);
  };

  const [loadingAddBeneficiary, setLoadingAddBeneficiary] = useState(false);
  const onBeneficiaryTopup = async (beneficiary_xid: string) => {
    setShowError(false);
    try {
      setLoadingAddBeneficiary(true);

      const body = {
        balance: balanceToAdd,
      };
      const response = await fetch(
        BASE_URL + "/api/v1/topup/beneficiary/" + beneficiary_xid,
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
        // throw new Error(response);
      }

      setForceFetchCtr(forceFetchCtr + 1);
    } catch (err: any) {
      setShowError(true);
      setErrorReason(err.message);
    } finally {
      setLoadingAddBeneficiary(false);
    }
  };

  const freq_add = [10, 20, 30, 50, 75, 100];

  return (
    <>
      <div
        className="cursor-pointer text-indigo-600 hover:text-indigo-900 group flex relative"
        onClick={() => setShowModal(true)}
      >
        <span className="group-hover:opacity-100 transition-opacity bg-indigo-500 px-1 text-sm text-indigo-100 rounded-md absolute -translate-x-1/2 -translate-y-8 opacity-0 m-4 mx-auto">
          TopUp
        </span>
        <span className="p-1">
          <SVGTopUp className="w-6 h-6 " />
        </span>
      </div>

      {showModal ? (
        <>
          <div className="font-normal justify-center items-center flex overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none">
            <div className="relative w-auto my-6 mx-auto max-w-3xl">
              <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
                {showError ? (
                  <div className=" border-red-400 rounded-b bg-red-100 px-4 py-3 text-red-700">
                    <p>Unable to Topup beneficiary</p>
                    <p className="text-xs">{errorReason}</p>
                  </div>
                ) : (
                  ""
                )}

                <div className="flex items-start justify-between p-5 border-b border-solid  rounded-t">
                  <div className="">
                    <h3 className="text-3xl font-semibold">
                      <span className="text-gray-400 ">TopUp: </span>
                      <span className="text-gray-700 ">
                        {beneficiary.data.nickname}
                      </span>
                    </h3>
                    <div className="text-sm text-gray-400 mt-2">
                      {beneficiary.data.email}
                    </div>
                  </div>
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
                    <div className="text-3xl ">
                      <span className="text-gray-700">
                        {beneficiary.data.balance}{" "}
                      </span>
                      <span className="text-gray-400">AED</span>
                    </div>
                    <div className="text-gray-400">Current Balance </div>
                  </div>
                  <div className="border-b "></div>

                  <div className="mt-6">
                    <div className="font-semibold">
                      How much would you like to add?
                    </div>

                    <input
                      className="mt-1 w-full text-center rounded border  p-2"
                      value={balanceToAdd}
                      type="text"
                      placeholder="100"
                      onChange={() => {}}
                    />

                    <div className="p-2"></div>
                    <div className="text-sm text-gray-400">
                      Accepted TopUps{" "}
                    </div>

                    <div className="flex justify-between">
                      {freq_add.map((val, idx) => {
                        return (
                          <div
                            key={idx}
                            className="m-1 cursor-pointer truncate rounded p-3 bg-indigo-50 text-indigo-600"
                            onClick={() => {
                              setShowError(false);
                              setBalanceToAdd(val);
                            }}
                          >
                            {val} AED
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  <div
                    className={
                      "mt-4 " + (balanceToAdd > 0 ? "" : " invisible ")
                    }
                  >
                    <button
                      className="bg-indigo-600 hover:bg-indigo-700 text-white  py-2 px-4 rounded"
                      type="button"
                      onClick={() => onBeneficiaryTopup(beneficiary.xid)}
                    >
                      TopUp Account
                      {loadingAddBeneficiary ? (
                        <LoadingSVG className="w-6 h-6 text-gray-300" />
                      ) : (
                        ""
                      )}
                    </button>
                    <div className="mt-3 text-gray-400 text-xs ">
                      A transaction fees of 1 AED will be applied when
                      processing this trasaction.
                    </div>
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
