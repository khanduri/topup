import { useEffect, useState } from "react";

import { BASE_URL } from "utils/xhr";
import { getStoredToken } from "utils/authentication";

import Dashboard from "components/dashboard_content";

import SidenavLayout from "pages/layout/sidenav";

import { BalanceCard, UsageCard, ActivityCard } from "components/cards";
import Title from "components/convention/title";

export default function Page() {
  const [loadingOptions, setLoadingOptions] = useState(false);
  const [allowedTopups, setAllowedTopups] = useState([0, 10, 25, 50, 75, 100]);

  const [loadingUserSummary, setLoadingUserSummary] = useState(false);
  const [userSummary, setUserSummary] = useState(null);

  const [loadingBeneficiaries, setLoadingBeneficiaries] = useState(false);
  const [beneficiaries, setBeneficiaries] = useState(null);

  const [forceFetchCtr, setForceFetchCtr] = useState(0);

  useEffect(() => {
    const fetchUserSummary = async () => {
      setLoadingUserSummary(true);
      try {
        const response = await fetch(BASE_URL + "/api/v1/topup/users", {
          method: "GET",
          headers: { Authorization: "Bearer " + getStoredToken() },
        });
        if (!response.ok) {
          throw new Error(`HTTP error: Status ${response.status}`);
        }
        let response_data = await response.json();

        setUserSummary(response_data.data);
      } catch (err) {
      } finally {
        setLoadingUserSummary(false);
      }
    };
    fetchUserSummary();

    const fetchBeneficiaries = async () => {
      setLoadingBeneficiaries(true);
      try {
        const response = await fetch(BASE_URL + "/api/v1/topup/beneficiary", {
          method: "GET",
          headers: { Authorization: "Bearer " + getStoredToken() },
        });
        if (!response.ok) {
          throw new Error(`HTTP error: Status ${response.status}`);
        }
        let response_data = await response.json();
        setBeneficiaries(response_data.data.beneficiaries);
      } catch (err) {
      } finally {
        setLoadingBeneficiaries(false);
      }
    };
    fetchBeneficiaries();

    const fetchTopupOptions = async () => {
      setLoadingOptions(true);
      try {
        const response = await fetch(BASE_URL + "/api/v1/topup/options", {
          method: "GET",
          headers: { Authorization: "Bearer " + getStoredToken() },
        });
        if (!response.ok) {
          throw new Error(`HTTP error: Status ${response.status}`);
        }
        let response_data = await response.json();
        const aedOptions = response_data.data.options.filter(
          (itm: { currency: string }) => itm.currency === "AED"
        );
        setAllowedTopups(aedOptions[0].denominations);
      } catch (err) {
      } finally {
        setLoadingOptions(false);
      }
    };
    fetchTopupOptions();
  }, [forceFetchCtr]);

  const runCleanSlate = async () => {
    try {
      const response = await fetch(BASE_URL + "/api/v1/topup/cleanslate", {
        method: "GET",
        headers: {
          Authorization: "Bearer " + getStoredToken(),
          "Content-Type": "application/json",
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error: Status ${response.status}`);
      }
      let response_data = await response.json();
      setForceFetchCtr(forceFetchCtr + 1);
    } catch (err) {
    } finally {
    }
  };
  const runBootstrap = async () => {
    try {
      const response = await fetch(BASE_URL + "/api/v1/topup/bootstrap", {
        method: "GET",
        headers: {
          Authorization: "Bearer " + getStoredToken(),
          "Content-Type": "application/json",
        },
      });
      if (!response.ok) {
        throw new Error(`HTTP error: Status ${response.status}`);
      }
      let response_data = await response.json();
      setForceFetchCtr(forceFetchCtr + 1);
    } catch (err) {
    } finally {
    }
  };

  return (
    <SidenavLayout>
      <Title type="sidenav-page">
        <div className="flex justify-between">
          Dashboard
          <div className="text-xs text-right">
            <span className="text-gray-400">Helpers functions: </span>
            <button
              className="m-2 p-2 rounded bg-red-600 text-white"
              onClick={runCleanSlate}
            >
              Reset All Data
            </button>
            <button
              className="m-2 p-2 rounded bg-blue-600 text-white"
              onClick={runBootstrap}
            >
              Populate Sample Data
            </button>
          </div>
        </div>
      </Title>

      <div className="grid grid-cols-1 gap-5 mt-6 sm:grid-cols-2 lg:grid-cols-4">
        <BalanceCard
          userSummary={userSummary}
          forceFetchCtr={forceFetchCtr}
          setForceFetchCtr={setForceFetchCtr}
        />
        <UsageCard userSummary={userSummary} />
        <ActivityCard userSummary={userSummary} />
      </div>

      <Dashboard
        beneficiaries={beneficiaries}
        allowedTopups={allowedTopups}
        forceFetchCtr={forceFetchCtr}
        setForceFetchCtr={setForceFetchCtr}
      />
    </SidenavLayout>
  );
}
