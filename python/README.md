LIVE @ https://topup-app.bytebeacon.com/

## Scope:

- I went beyond the scope of initial work and instead of just a REST API, I built an entire app that showcases how I write and design backend + frontend + infra.
- I built a fully functioning app based on the scope given that:
  - Allows a user to login into a TopUp system
  - Transfer fake funds into their TopUp account balance
  - Add beneficiaries
  - Use these funds to distribute funds to beneficiaries

## Assumptions:

- From a product point I wanted the user to enter as much information as they want (We get more data that way). So I placed the limit on "Active" beneficiaries at 5 adn allowed the user to add many "Inactive" beneficiaries to make the experience good. The user can choose to add all their informaiton (or import from a source) and pick the 5 "Active" beneficiaries to adhere to our limit
- No limit on Amount being credited to our topup account balance from their bank. And no charge for crediting your Topup Account when moving money from your bank.
- regarding: "The user's balance should be debited first before the top-up transaction is attempted.". This should be done in an atomic transaction and should not be done sequentially

## Backend:

#### Notes for devs:

- Start with: https://github.com/khanduri/topup/tree/main/python/api/src/micro_services/topup/apis
- Logic / Controller: https://github.com/khanduri/topup/tree/main/python/api/src/micro_services/topup/logic
- Data / Repository: https://github.com/khanduri/topup/tree/main/python/api/src/depot/topup

- The backend is written in Python / Flask and can scale very well as each API is stateless and requires context be passed via REST API
- The backend databases aceess are primarily done through a Repository pattern / Data access layer. All code will be under teh "Depot" module. This makes the services stateless. This is easier to test / maintain in the long run.
- Each "service" can be a separate deployment target for the future. This way we can keep all services in a single repo, but scale the application as we please in the future (This is a hybrid approach to monolith and SOA that helps in testing and staging setups as well). Happy to chat more about this if there are questions.
- The app is containarized using Docker. It's currently deployed on hekoru, but with any managed container service (ie: any managed k8s cluster) can be deoplyed to any public cloud (AWS, GCP, Azure) rather easily. Sample files on deplying to GCP are provided in the `infra` forlder

## Frontend:

#### Notes for devs:

- The frontend is written in React / tailwind and is responsive in nature
- It's written as a SPA (Single page application)
- The current deployment flow, to make this prod ready is building static production files and served over popular CDN nodes. The frontend code is backend agnostic and only talks to the API's exposed.
