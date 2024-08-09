

class OptionsLogic(object):
    
    @classmethod
    def fetch_topup_options(cls, organization_xid, user_xid):

        payload = {
            'organization_xid': organization_xid,
            'user_xid': user_xid,
            # TODO: move this to config or db so we don't have to deploy everytime we need to make a change
            # NOTE: flexibility to add more currencies and denominations in the future
            'options': [
                {
                    'currency': 'AED',
                    'denominations': [0,5,10,20,30,50,75,100],
                }
            ],
        }
        
        return payload
