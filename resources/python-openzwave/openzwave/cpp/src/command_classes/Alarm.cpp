//-----------------------------------------------------------------------------
//
//	Alarm.cpp
//
//	Implementation of the Z-Wave COMMAND_CLASS_ALARM
//
//	Copyright (c) 2010 Mal Lansell <openzwave@lansell.org>
//
//	SOFTWARE NOTICE AND LICENSE
//
//	This file is part of OpenZWave.
//
//	OpenZWave is free software: you can redistribute it and/or modify
//	it under the terms of the GNU Lesser General Public License as published
//	by the Free Software Foundation, either version 3 of the License,
//	or (at your option) any later version.
//
//	OpenZWave is distributed in the hope that it will be useful,
//	but WITHOUT ANY WARRANTY; without even the implied warranty of
//	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//	GNU Lesser General Public License for more details.
//
//	You should have received a copy of the GNU Lesser General Public License
//	along with OpenZWave.  If not, see <http://www.gnu.org/licenses/>.
//
//-----------------------------------------------------------------------------

#include "command_classes/CommandClasses.h"
#include "command_classes/Alarm.h"
#include "Defs.h"
#include "Msg.h"
#include "Node.h"
#include "Driver.h"
#include "platform/Log.h"

#include "value_classes/ValueByte.h"
#include "value_classes/ValueRaw.h"

using namespace OpenZWave;

enum AlarmCmd
{
	AlarmCmd_Get			= 0x04,
	AlarmCmd_Report			= 0x05,
	// Version 2
	AlarmCmd_SupportedGet		= 0x07,
	AlarmCmd_SupportedReport	= 0x08
};

enum
{
	AlarmIndex_Type = 0,
	AlarmIndex_Level,
	AlarmIndex_SourceNodeId,
	AlarmIndex_Notification
};

enum
{
	Alarm_General = 0,
	Alarm_Smoke,
	Alarm_CarbonMonoxide,
	Alarm_CarbonDioxide,
	Alarm_Heat,
	Alarm_Flood,
	Alarm_Access_Control,
	Alarm_Burglar,
	Alarm_Power_Management,
	Alarm_System,
	Alarm_Emergency,
	Alarm_Clock,
	Alarm_Appliance,
	Alarm_HomeHealth,
	Alarm_Count
};

static char const* c_alarmTypeName[] =
{
		"General",
		"Smoke",
		"Carbon Monoxide",
		"Carbon Dioxide",
		"Heat",
		"Flood",
		"Access Control",
		"Burglar",
		"Power Management",
		"System",
		"Emergency",
		"Clock",
		"Appliance",
		"HomeHealth"
};

//-----------------------------------------------------------------------------
// <WakeUp::WakeUp>
// Constructor
//-----------------------------------------------------------------------------
Alarm::Alarm
(
		uint32 const _homeId,
		uint8 const _nodeId
):
CommandClass( _homeId, _nodeId )
{
	SetStaticRequest( StaticRequest_Values );
}


//-----------------------------------------------------------------------------
// <Alarm::RequestState>
// Request current state from the device
//-----------------------------------------------------------------------------
bool Alarm::RequestState
(
		uint32 const _requestFlags,
		uint8 const _instance,
		Driver::MsgQueue const _queue
)
{
	if( ( _requestFlags & RequestFlag_Static ) && HasStaticRequest( StaticRequest_Values ) )
	{
		if( GetVersion() > 1 )
		{
			// Request the supported alarm types
			Msg* msg = new Msg( "AlarmCmd_SupportedGet", GetNodeId(), REQUEST, FUNC_ID_ZW_SEND_DATA, true, true, FUNC_ID_APPLICATION_COMMAND_HANDLER, GetCommandClassId() );
			msg->SetInstance( this, _instance );
			msg->Append( GetNodeId() );
			msg->Append( 2 );
			msg->Append( GetCommandClassId() );
			msg->Append( AlarmCmd_SupportedGet );
			msg->Append( GetDriver()->GetTransmitOptions() );
			GetDriver()->SendMsg( msg, _queue );
			return true;
		}
	}

	if( _requestFlags & RequestFlag_Dynamic )
	{
		return RequestValue( _requestFlags, 0, _instance, _queue );
	}

	return false;
}

//-----------------------------------------------------------------------------
// <Alarm::RequestValue>
// Request current value from the device
//-----------------------------------------------------------------------------
bool Alarm::RequestValue
(
		uint32 const _requestFlags,
		uint8 const _dummy1,	// = 0 (not used)
		uint8 const _instance,
		Driver::MsgQueue const _queue
)
{
	if( IsGetSupported() )
	{
		if( GetVersion() == 1 )
		{
			Msg* msg = new Msg( "AlarmCmd_Get", GetNodeId(), REQUEST, FUNC_ID_ZW_SEND_DATA, true, true, FUNC_ID_APPLICATION_COMMAND_HANDLER, GetCommandClassId() );
			msg->SetInstance( this, _instance );
			msg->Append( GetNodeId() );
			msg->Append( 2 );
			msg->Append( GetCommandClassId() );
			msg->Append( AlarmCmd_Get );
			msg->Append( GetDriver()->GetTransmitOptions() );
			GetDriver()->SendMsg( msg, _queue );
			return true;
		}
		else
		{
			bool res = false;
			for( uint8 i = 0; i < Alarm_Count; i++ )
			{
				if( Value* value = GetValue( _instance, i + 3 ) ) {
					value->Release();
					Msg* msg = new Msg( "AlarmCmd_Get", GetNodeId(), REQUEST, FUNC_ID_ZW_SEND_DATA, true, true, FUNC_ID_APPLICATION_COMMAND_HANDLER, GetCommandClassId() );
					msg->SetInstance( this, _instance );
					msg->Append( GetNodeId() );
					msg->Append( GetVersion() == 2 ? 4 : 5);
					msg->Append( GetCommandClassId() );
					msg->Append( AlarmCmd_Get );
					msg->Append( 0x00); // ? proprietary alarm ?
					msg->Append( i );
					if( GetVersion() > 2 )
						msg->Append(0x01); //get first event of type.
					msg->Append( GetDriver()->GetTransmitOptions() );
					GetDriver()->SendMsg( msg, _queue );
					res = true;
				}
			}
			return res;
		}
	} else {
		Log::Write(  LogLevel_Info, GetNodeId(), "AlarmCmd_Get Not Supported on this node");
	}
	return false;
}

//-----------------------------------------------------------------------------
// <Alarm::HandleMsg>
// Handle a message from the Z-Wave network
//-----------------------------------------------------------------------------
bool Alarm::HandleMsg
(
		uint8 const* _data,
		uint32 const _length,
		uint32 const _instance	// = 1
)
{
	if (AlarmCmd_Report == (AlarmCmd)_data[0])
	{
		// We have received a report from the Z-Wave device
		if( GetVersion() == 1 )
		{
			Log::Write( LogLevel_Info, GetNodeId(), "Received Alarm report: type=%d, level=%d", _data[1], _data[2] );
		}
		else
		{
			string alarm_type =  ( _data[5] < Alarm_Count ) ? c_alarmTypeName[_data[5]] : "Unknown type";

			Log::Write( LogLevel_Info, GetNodeId(), "Received Alarm report: type=%d, level=%d, sensorSrcID=%d, type:%s event:%d, status=%d",
							_data[1], _data[2], _data[3], alarm_type.c_str(), _data[6], _data[4] );
		}
		ValueByte* value;
		if( (value = static_cast<ValueByte*>( GetValue( _instance, AlarmIndex_Type ) )) )
		{
			value->OnValueRefreshed( _data[1] );
			value->Release();
		}
		if( (value = static_cast<ValueByte*>( GetValue( _instance, AlarmIndex_Level ) )) )
		{
			value->OnValueRefreshed( _data[2] );
			value->Release();
		}

		// With Version=2, the data has more detailed information about the alarm
		if(( GetVersion() > 1 ) && ( _length >= 7  ))
		{
			if( (value = static_cast<ValueByte*>( GetValue( _instance, AlarmIndex_SourceNodeId ) )) )
			{
				value->OnValueRefreshed( _data[3] );
				value->Release();
			}

			if( (value = static_cast<ValueByte*>( GetValue( _instance, _data[5]+3 ) )) )
			{
				value->OnValueRefreshed( _data[6] );
				value->Release();
			}
			if (_data[5] == 6)
			{
				if( (value = static_cast<ValueByte*>( GetValue( _instance, 0x99 ) )) )
				{
					value->OnValueRefreshed( _data[8] );
					value->Release();
				}
                if( ValueRaw* value = static_cast<ValueRaw*>( GetValue( _instance, 0x98 ) ) )
				{
				   uint8 data[_data[7]];
                   int8 size =  _data[7];	
                   if (size > 0) {
						memcpy( data, &_data[8], size );
					} else {
						size = 1;
						data[0] = 0;
					}
                  
                  	value->OnValueRefreshed( data, size );
					value->Release();
				}
			}
		}

		return true;
	}

	if( AlarmCmd_SupportedReport == (AlarmCmd)_data[0] )
	{
		if( Node* node = GetNodeUnsafe() )
		{
			// We have received the supported alarm types from the Z-Wave device
			Log::Write( LogLevel_Info, GetNodeId(), "Received supported alarm types" );

			node->CreateValueByte( ValueID::ValueGenre_User, GetCommandClassId(), _instance, AlarmIndex_SourceNodeId, "SourceNodeId", "", true, false, 0, 0 );
			Log::Write( LogLevel_Info, GetNodeId(), "    Added alarm SourceNodeId" );

			// Parse the data for the supported alarm types
			uint8 numBytes = _data[1];
			for( uint32 i=0; i<numBytes; ++i )
			{
				for( int32 bit=0; bit<8; ++bit )
				{
					if( ( _data[i+2] & (1<<bit) ) != 0 )
					{
						int32 index = (int32)(i<<3) + bit;
						if( index < Alarm_Count )
						{
							node->CreateValueByte( ValueID::ValueGenre_User, GetCommandClassId(), _instance, index+3, c_alarmTypeName[index], "", true, false, 0, 0 );
							Log::Write( LogLevel_Info, GetNodeId(), "    Added alarm type: %s", c_alarmTypeName[index] );
							if (index == 6)
							{
                              	uint8 data[10];
								memset( data, 0, 10 );
								node->CreateValueByte( ValueID::ValueGenre_User, GetCommandClassId(), _instance, 0x99, "Memory Code User", "", true, false, 0, 0 );
                                node->CreateValueRaw( ValueID::ValueGenre_User, GetCommandClassId(), _instance, 0x98, "Raw Code User", "", true, false, data, 10, 0 );
							}
						} else {
							Log::Write( LogLevel_Info, GetNodeId(), "    Unknown alarm type: %d", index );
						}
					}
				}
			}
		}

		ClearStaticRequest( StaticRequest_Values );
		return true;
	}

	return false;
}

//-----------------------------------------------------------------------------
// <Alarm::SetValue>
// Set a new value for the switch    (UGLY HACK FOR NOW)
//-----------------------------------------------------------------------------
bool Alarm::SetValue
(
	Value const& _value
)
{
	uint8 instance = _value.GetID().GetInstance();

	switch( _value.GetID().GetIndex() )
	{
		case AlarmIndex_Notification:
		{
			ValueByte const* value = static_cast<ValueByte const*>(&_value);
			Log::Write( LogLevel_Info, GetNodeId(), "AlarmNotification::Set - Setting node %d to %d", GetNodeId(), value->GetValue());
			Msg* msg = new Msg( "AlarmNotification_Set", GetNodeId(), REQUEST, FUNC_ID_ZW_SEND_DATA, true );
			msg->SetInstance( this, instance );
			msg->Append( GetNodeId() );
			msg->Append( 3 );
			msg->Append( GetCommandClassId() );
			msg->Append( AlarmCmd_Report );
			msg->Append( 0x00 );
			msg->Append( 0x00 );
			msg->Append( 0x00 );
			msg->Append( 0x00 );
			switch( value->GetValue() )
				{
					case 1:
						{
							msg->Append( 0x07 );
							msg->Append( 0x01 );
							break;
						}
					case 2:
						{
							msg->Append( 0x0A );
							msg->Append( 0x02 );
							break;
						}
					case 3:
						{
							msg->Append( 0x0A );
							msg->Append( 0x03 );
							break;
						}
					case 4:
						{
							msg->Append( 0x0A );
							msg->Append( 0x01 );
							break;
						}
					case 5:
						{
							msg->Append( 0x06 );
							msg->Append( 0x16 );
							break;
						}
					case 6:
						{
							msg->Append( 0x0A );
							msg->Append( 0x05 );
							break;
						}
					default:
						{
							msg->Append( 0x07 );
							msg->Append( 0x01 );
							break;
						}
				}
				msg->Append( 0x00 );
				msg->Append( 0x00 );
				msg->Append( GetDriver()->GetTransmitOptions() );
				GetDriver()->SendMsg( msg, Driver::MsgQueue_Send );
				return true;
				break;
		}
	}
	return false;
}

//-----------------------------------------------------------------------------
// <Alarm::CreateVars>
// Create the values managed by this command class
//-----------------------------------------------------------------------------
void Alarm::CreateVars
(
		uint8 const _instance
)
{
	if( Node* node = GetNodeUnsafe() )
	{
		node->CreateValueByte( ValueID::ValueGenre_User, GetCommandClassId(), _instance, AlarmIndex_Type, "Alarm Type", "", true, false, 0, 0 );
		node->CreateValueByte( ValueID::ValueGenre_User, GetCommandClassId(), _instance, AlarmIndex_Level, "Alarm Level", "", true, false, 0, 0 );
		node->CreateValueByte( ValueID::ValueGenre_User, GetCommandClassId(), _instance, AlarmIndex_Notification, "Alarm Notification", "", false, true, 0, 0 );
	}
}