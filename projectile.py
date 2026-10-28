from matplotlib.animation import FuncAnimation                                   #for animation 
import math
import matplotlib.pyplot as plt                                                     #for potting graphs
import time as clock


def velocity_components(u, theta):
    theta_rad = math.radians(theta)
    ux = u * math.cos(theta_rad)
    uy = u * math.sin(theta_rad)
    return ux, uy


def max_height(u, theta, g):
    theta_rad = math.radians(theta)
    H = (u**2 * math.sin(theta_rad)**2) / (2 * g)
    return H


def time_of_flight(u, theta, g):
    theta_rad = math.radians(theta)
    T = (2 * u * math.sin(theta_rad)) / g
    return T


def range_pro(u, theta, g):
    theta_rad = math.radians(theta)
    R = (u**2 * 2 * math.sin(theta_rad) * math.cos(theta_rad)) / g
    return R


def simulate_motion(u, theta, g):
    T = time_of_flight(u, theta, g)
    ux, uy = velocity_components(u, theta)

    x = []
    y = []
    times=[]
    
    for i in range(0, 101):
        t = T * i / 100

        x_value = ux * t
        y_value = uy * t - 0.5 * g * t**2

        x.append(x_value)
        y.append(y_value)
        times.append(t)
    
    return x, y, times


# Main program
g = 9.8

u = float(input("Enter initial velocity (m/s): "))
angles=[]
for i in range(3):
    while True:
        angle = float(input("Enter angle: "))

        if 0 <= angle <= 90:
            angles.append(angle)
            break
        else:
            print("Invalid angle. Enter an angle between 0 and 90 degrees.")

max_T = max(time_of_flight(u, theta, g) for theta in angles)     #max time among the three projectiles

dt=0.01
frames=int(max_T/dt)+1

fps=50
interval=1000/fps

trajectories=[]
for theta in angles:
    x,y,times=simulate_motion(u,theta,g)
    trajectories.append((theta,x,y,times))



results=[]
for theta in angles:
    height=max_height(u,theta,g)                                                    
    time=time_of_flight(u, theta, g)                                                
    range_value=range_pro(u, theta, g)
                                                                                    
    results.append([theta,height,time,range_value])                                                                                #T2 = time_of_flight(u, theta2, g)
                                                                                    

                                                                                   
best_range = max(result[3] for result in results)
for result in results:
    if result[3] == best_range:
        best_angle = result[0]


print(f"Best angle for range: {best_angle}°")    

print("Angle    Height(m)    Time(s)    Range(m)")

for result in results:
    theta = result[0]
    height = result[1]
    time = result[2]
    range_value = result[3]

    print(f"{theta}°".ljust(10) + f"{height:<15.2f}{time:<12.2f}{range_value:<12.2f}")

for theta,x,y,times in trajectories:
    if theta==best_angle:
        plt.plot(x,y,linewidth="3",label=f"Best Range={theta}°")
    else:
        plt.plot(x,y,label=f"{theta}°")

    T=time_of_flight(u,theta,g)                                      #Marking the max height point for better visualization
    t_max=T/2
    ux, uy = velocity_components(u, theta)
    x_max_height = ux * t_max
    height = max_height(u, theta, g)
    plt.scatter(x_max_height,height)

    plt.annotate(
        f"Max: {height:.1f} m",
        (x_max_height, height)
        )
plt.xlabel("Horizontal distance in (m)")
plt.ylabel("Height in (m)")
plt.title("Projectile Motion Comparision")
plt.grid()
plt.legend()

max_x = max(max(x) for _, x, _, _ in trajectories)
max_y = max(max(y) for _, _, y, _ in trajectories)
plt.xlim(0,max_x*1.1)
plt.ylim(0,max_y*1.1)

points=[]

for theta,x,y,times in trajectories:
    point, =plt.plot([],[],"o")    #for creating frame: [],[] are the x and y coordinates initially empty and "o" is the shape of the trajectory you want
    points.append(point)
                   
start_time=clock.time()

time_text = plt.text(0.02,0.95,'',transform=plt.gca().transAxes)

velocity_texts = []

fig=plt.gcf()

for i, (theta,x,y,times) in enumerate(trajectories):
    text=fig.text(
        0.02,
        0.94 - i*0.04,
        ''
    )
    velocity_texts.append(text)


max_flight_time=max(result[2] for result in results)

def update(frame):                              #tells Python where the projectile should be at each moment.
    current_time=min(clock.time()-start_time,max_flight_time)
    time_text.set_text(f"Time:{current_time:.2f}")    
    for i, point in enumerate(points):
        theta=trajectories[i][0]
        ux,uy=velocity_components(u,theta)
        vx=ux
        vy=uy-g*current_time
        velocity_texts[i].set_text(
            f"{theta}°  Vx: {vx:.2f} m/s  Vy: {vy:.2f} m/s"
        )
        x=ux*current_time
        y=uy*current_time-0.5*g*current_time**2

        if y>=0:
            point.set_data([x],[y])
        else:
            point.set_data([],[])    
        
    return points + [time_text] + velocity_texts

plt.subplots_adjust(top=0.78)
ani=FuncAnimation(
    plt.gcf(),
    update,
    frames=frames,
    interval=interval
)

plt.show()
