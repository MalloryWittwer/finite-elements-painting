import numpy as np
import plotly.express as px
import plotly.graph_objs as go

class Simulation:
    
    def __init__(self):       
        self.init_temp = 1
        self.n_x = 60
        self.n_y = 60
        
        self.reset()
        
    def reset(self):
        self.heat_sources = []
        self.T = np.ones((self.n_x * self.n_y)) * self.init_temp
        
    def add_heat_source(self, loc, sign, intensity=1.0):
        self.heat_sources.append({
            'loc': loc, 
            'intensity': intensity * sign
        })
        
    def set_heat_source_mask(self, binary_array, sign):
        for loc, val in enumerate(binary_array.ravel()):
            if val:
                self.add_heat_source(loc, sign)
    
    def step(self):
        dt = 0.25
        alpha = 1e-3
        
        C = self.T.copy()        
        
        n = 0
        m = 1 - self.n_x
    
        for k in range(self.T.size):
            if (k==0):
                # South-West corner
                C[k] = self.T[k] * (1 - 4 * dt * (alpha + 1)) + 4 * dt * alpha * self.init_temp + 2 * dt * (self.T[k + self.n_x] + self.T[k + 1])
                
            elif (k==self.n_x*(self.n_y-1)):
                # Nord-West corner
                C[k] = self.T[k]*(1-4*dt*(alpha+1)) + 4*dt*alpha*self.init_temp + 2*dt*(self.T[k-self.n_x]+self.T[k+1])
                
            elif (k==self.n_x*self.n_y-1):
                # Nord-East corner
                C[k] = self.T[k]*(1-4*dt*(alpha+1)) + 4*dt*alpha*self.init_temp + 2*dt*(self.T[k-self.n_x]+self.T[k-1])
            elif (k==self.n_x-1):
                # South-West corner
                C[k] = self.T[k]*(1-4*dt*(alpha+1)) + 4*dt*alpha*self.init_temp + 2*dt*(self.T[k+self.n_x]+self.T[k-1])
                
            elif (k<self.n_x-1):
                # South border
                C[k] = self.T[k]*(1-2*dt*(alpha+2)) + 2*dt*alpha*self.init_temp + 2*dt*(self.T[k+self.n_x] + self.T[k+1]/2 + self.T[k-1]/2)
                
            elif ((self.n_x*self.n_y-k)<self.n_x):
                # Nord border
                C[k] = self.T[k]*(1-2*dt*(alpha+2)) + 2*dt*alpha*self.init_temp + 2*dt*(self.T[k-self.n_x] + self.T[k+1]/2 + self.T[k-1]/2)
                
            elif (n==self.n_x and k!=self.n_x*(self.n_y-1)):
                # West border
                C[k] = self.T[k]*(1-2*dt*(alpha+2)) + 2*dt*alpha*self.init_temp + 2*dt*(self.T[k+1] + self.T[k+self.n_x]/2 + self.T[k-self.n_x]/2)
                n = 0
                
            elif (m==self.n_x):
                # East border
                C[k] = self.T[k]*(1-2*dt*(alpha+2)) + 2*dt*alpha*self.init_temp + 2*dt*(self.T[k-1] + self.T[k+self.n_x]/2 + self.T[k-self.n_x]/2)
                m = 0
            
            else:
                # Other nodes
                C[k] = self.T[k]*(1-4*dt) + dt*(self.T[k+1] + self.T[k-1] + self.T[k+self.n_x] + self.T[k-self.n_x])
                
            # Heat sources
            if len(self.heat_sources):
                # print('HEAT SOURCE LENGTH:', len(self.heat_sources))
                for hs in self.heat_sources:
                    if (k == hs['loc']):
                        C[k] = self.T[k]*(1-4*dt) + dt*(self.T[k+1] + self.T[k-1] + self.T[k+self.n_x] + self.T[k-self.n_x]) + dt * hs['intensity']
                
            n += 1
            m += 1
                        
        self.T = C.copy()
        
    def get_heatmap(self):
        fig = px.imshow(self.T.reshape((self.n_x, self.n_y)))#, zmin=self.init_temp, zmax=2 * self.init_temp)
        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)
        fig.update_traces(showscale=False)
        fig.update_coloraxes(showscale=False)
        fig.update_layout(
            margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
            autosize=False,
            width=500,
            height=500,
            paper_bgcolor="black"
        )
        return fig
                        
if __name__ == '__main__':
    s = Simulation()
    for _ in range(100):
        s.step()
    fig = s.get_heatmap()
    fig.show()

