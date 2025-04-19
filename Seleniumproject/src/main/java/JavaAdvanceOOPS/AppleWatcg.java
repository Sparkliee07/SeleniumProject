package JavaAdvanceOOPS;

public abstract class AppleWatcg implements SmartWatch {

	public AppleWatcg()
	{
		
	}
	@Override
	public String getDataTime() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void setDateTime(String newDate) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public boolean changeBattery() {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public int getBatteryPercentage() {
		// TODO Auto-generated method stub
		return 0;
	}

	@Override
	public String getStrapColor() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Boolean connectToPhone() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public boolean turnBluetooth() {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public int getStepCount() {
		// TODO Auto-generated method stub
		return 0;
	}

	@Override
	public int getHeartBeat() {
		// TODO Auto-generated method stub
		return 0;
	}

	@Override
	public void setGoal(int steps) {
		// TODO Auto-generated method stub
		
	}
	public abstract void BPM();
	

}
