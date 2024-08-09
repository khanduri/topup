import { Console } from "console";
import React, { ChangeEventHandler, useState, useEffect } from "react";

import { getStoredToken } from "utils/authentication";
import { BASE_URL } from "utils/xhr";
import LoadingSVG from "images/loading";

export default function Modal(props: any) {
  const { allowedTopups, beneficiaries, forceFetchCtr, setForceFetchCtr } =
    props;

  const [showModal, setShowModal] = useState(false);
  const [name, setName] = useState("");
  const [validName, setValidName] = useState(false);
  const [email, setEMail] = useState("");
  const [validEmail, setValidEmail] = useState(false);
  const [balanceToAdd, setBalanceToAdd] = useState(0);

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setBalanceToAdd(parseInt(e.target.value || "0") || 0);
  };
  const onNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setName(e.target.value);
    setValidName(e.target.value !== "" && e.target.value.length <= 20);
  };
  const onEmailChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const inputemail = e.target.value;
    setEMail(inputemail);
    const emailRegex = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i;
    setValidEmail(emailRegex.test(inputemail));
  };

  const [loadingAddBeneficiary, setLoadingAddBeneficiary] = useState(false);
  const onBeneficiaryAdd = async () => {
    try {
      setLoadingAddBeneficiary(true);

      const body = {
        nickname: name,
        email: email,
        balance: balanceToAdd,
      };
      const response = await fetch(BASE_URL + "/api/v1/topup/beneficiary", {
        method: "POST",
        headers: {
          Authorization: "Bearer " + getStoredToken(),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ data: body }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error: Status ${response.status}`);
      }
      let response_data = await response.json();

      // console.log(response_data);
      setForceFetchCtr(forceFetchCtr + 1);
    } catch (err) {
    } finally {
      setLoadingAddBeneficiary(false);
    }
  };

  let active_b = [];
  if (beneficiaries) {
    active_b = beneficiaries.filter((item: any) => item.data.active);
  }

  return (
    <>
      <button
        className="bg-indigo-500 hover:bg-indigo-700 text-white py-2 px-4 rounded"
        type="button"
        onClick={() => setShowModal(true)}
      >
        Add Beneficiary
      </button>
      {showModal ? (
        <>
          <div className="justify-center items-center flex overflow-x-hidden overflow-y-auto fixed inset-0 z-50 outline-none focus:outline-none">
            <div className="relative w-auto my-6 mx-auto max-w-3xl">
              <div className="border-0 rounded-lg shadow-lg relative flex flex-col w-full bg-white outline-none focus:outline-none">
                <div className="flex items-start justify-between p-5 border-b border-solid  rounded-t">
                  <h3 className="text-3xl font-semibold">Add Beneficiary</h3>
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
                  <div className="mb-4">
                    <div className="flex justify-between ">
                      <div className="text-left">
                        <div className="text-3xl text-gray-700">
                          {active_b.length}
                        </div>
                        <div className="text-xs text-red-300">5 allowed</div>
                        <div className="text-gray-400">
                          Active Beneficiaries
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-3xl text-gray-700">
                          {beneficiaries.length}
                        </div>
                        <div className="text-xs text-red-400">&nbsp;</div>
                        <div className="text-gray-400">Total Beneficiaries</div>
                      </div>
                    </div>
                  </div>
                  <div className="border-b "></div>

                  <div className="mt-6">
                    <div className="font-semibold">
                      Who would you like to add?
                    </div>
                    <div>
                      <input
                        className="mt-1 w-full rounded border  p-2"
                        value={name}
                        type="text"
                        placeholder="Nickname "
                        onChange={onNameChange}
                      />
                      <input
                        className="mt-1 w-full rounded border  p-2"
                        value={email}
                        type="text"
                        placeholder="Email "
                        onChange={onEmailChange}
                      />
                      <input
                        className="mt-1 w-full rounded border  p-2"
                        value={balanceToAdd === 0 ? "" : balanceToAdd}
                        type="text"
                        placeholder="TopUp: 0 if left blank"
                        onChange={onChange}
                      />
                    </div>
                    <div className="p-2"></div>
                    <div className="text-sm text-gray-400">
                      Allowed denominations{" "}
                    </div>

                    <div className="flex justify-between">
                      {allowedTopups.map((val: number, idx: number) => {
                        return (
                          <div
                            key={idx}
                            className="m-1 cursor-pointer truncate rounded p-3 bg-indigo-50 text-indigo-500"
                            onClick={() => setBalanceToAdd(val)}
                          >
                            {val} AED
                          </div>
                        );
                      })}
                    </div>
                    <div className="mt-3 text-gray-400 text-xs ">
                      A transaction fees of 1 AED will be applied when adding
                      topup balance.
                    </div>
                  </div>

                  <div
                    className={
                      "mt-4 " + (validName && validEmail ? "" : " invisible ")
                    }
                  >
                    <button
                      className="bg-green-600 hover:bg-green-700 text-white  py-2 px-4 rounded"
                      type="button"
                      onClick={() => onBeneficiaryAdd()}
                    >
                      Add Beneficiary
                      {loadingAddBeneficiary ? (
                        <LoadingSVG className="w-6 h-6 text-gray-300" />
                      ) : (
                        ""
                      )}
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
