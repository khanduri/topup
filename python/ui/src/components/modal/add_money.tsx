import React, { ChangeEventHandler, useEffect } from "react";

import { BASE_URL } from "utils/xhr";
import { getStoredToken } from "utils/authentication";
import LoadingSVG from "images/loading";

export default function Modal(props: any) {
  const { currentBalance, forceFetchCtr, setForceFetchCtr } = props;

  const [showModal, setShowModal] = React.useState(false);
  const [balanceToAdd, setBalanceToAdd] = React.useState(0);
  const [displayBalance, setDisplayBalance] = React.useState(currentBalance);

  useEffect(() => {
    setDisplayBalance(currentBalance);
  }, [currentBalance]);

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setBalanceToAdd(parseInt(e.target.value || "0") || 0);
  };

  const [loadingAddBalance, setLoadingAddBalance] = React.useState(false);
  const addBalance = async () => {
    setLoadingAddBalance(true);
    try {
      const body = { action: "BALANCE_ADD", action_data: balanceToAdd };
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
      setDisplayBalance(response_data.data.user_state.data.balance);
      setForceFetchCtr(forceFetchCtr + 1);
    } catch (err) {
    } finally {
      setLoadingAddBalance(false);
    }
  };

  const freq_add = [100, 500, 1000, 2000];

  return (
    <>
      <button
        className="bg-indigo-500 hover:bg-indigo-700 text-white  py-2 px-4 rounded"
        type="button"
        onClick={() => setShowModal(true)}
      >
        Add Money
      </button>
      {showModal ? (
        <>
          <div className="justify-center items-center flex overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none">
            <div className="relative w-auto my-6 mx-auto max-w-3xl">
              <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
                <div className="flex items-start justify-between p-5 border-b border-solid  rounded-t">
                  <h3 className="text-3xl font-semibold">Add Money</h3>
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
                    <div className="text-3xl text-gray-700">
                      {displayBalance} AED
                    </div>
                    <div className="text-gray-400">Current Balance </div>
                  </div>
                  <div className="border-b "></div>

                  <div className="mt-6">
                    <div className="font-semibold">
                      How much would you like to add?
                    </div>
                    <div>
                      <input
                        className="mt-1 w-full rounded border  p-2"
                        value={balanceToAdd === 0 ? "" : balanceToAdd}
                        type="text"
                        placeholder="100"
                        onChange={onChange}
                      />
                    </div>
                    <div className="p-2"></div>
                    <div className="text-sm text-gray-400">
                      Frequently Used{" "}
                    </div>

                    <div className="flex justify-between">
                      {freq_add.map((val, idx) => {
                        return (
                          <div
                            key={idx}
                            className="m-1 cursor-pointer truncate rounded p-3 bg-indigo-50 text-indigo-600"
                            onClick={() => setBalanceToAdd(val)}
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
                      className="bg-green-600 hover:bg-green-700 text-white  py-2 px-4 rounded"
                      type="button"
                      onClick={() => addBalance()}
                      disabled={loadingAddBalance}
                    >
                      Add to account
                      {loadingAddBalance ? (
                        <LoadingSVG className="w-8 h-8 text-gray-300" />
                      ) : (
                        ""
                      )}
                    </button>
                    <div className="mt-3 text-gray-400 text-sm">
                      This will be debited from your bank account and added to
                      your TopUp balance!
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
