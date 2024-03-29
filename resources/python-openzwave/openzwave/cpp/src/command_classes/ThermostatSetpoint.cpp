//-----------------------------------------------------------------------------
//
//	ThermostatSetpoint.cpp
//
//	Implementation of the Z-Wave COMMAND_CLASS_THERMOSTAT_SETPOINT
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
#include "command_classes/ThermostatSetpoint.h"
#include "Defs.h"
#include "Msg.h"
#include "Node.h"
#include "Driver.h"
#include "platform/Log.h"

#include "value_classes/ValueDecimal.h"
#include "value_classes/ValueByte.h"

#include "tinyxml.h"

using namespace OpenZWave;

enum ThermostatSetpointCmd
{
	ThermostatSetpointCmd_Set				= 0x01,
	ThermostatSetpointCmd_Get				= 0x02,
	ThermostatSetpointCmd_Report			= 0x03,
	ThermostatSetpointCmd_SupportedGet		= 0x04,
	ThermostatSetpointCmd_SupportedReport	= 0x05,
	ThermostatSetpointCmd_CapabilitiesGet   = 0x09,
	ThermostatSetpointCmd_CapabilitiesReport = 0x0A
};

enum
{
	ThermostatSetpoint_Unused0	= 0,
	ThermostatSetpoint_Heating1,
	ThermostatSetpoint_Cooling1,
	ThermostatSetpoint_Unused3,
	ThermostatSetpoint_Unused4,
	ThermostatSetpoint_Unused5,
	ThermostatSetpoint_Unused6,
	ThermostatSetpoint_Furnace,
	ThermostatSetpoint_DryAir,
	ThermostatSetpoint_MoistAir,
	ThermostatSetpoint_AutoChangeover,
	ThermostatSetpoint_HeatingEcon,
	ThermostatSetpoint_CoolingEcon,
	ThermostatSetpoint_AwayHeating,
	ThermostatSetpoint_Count
};

static char const* c_setpointName[] =
{
	"Unused 0",
	"Heating 1",
	"Cooling 1",
	"Unused 3",
	"Unused 4",
	"Unused 5",
	"Unused 6",
	"Furnace",
	"Dry Air",
	"Moist Air",
	"Auto Changeover",
	"Heating Econ",
	"Cooling Econ",
	"Away Heating"
};

//-----------------------------------------------------------------------------
// <ThermostatSetpoint::ThermostatSetpoint>
// Constructor
//-----------------------------------------------------------------------------
ThermostatSetpoint::ThermostatSetpoint
(
	uint32 const _homeId,
	uint8 const _nodeId
):
	CommandClass( _homeId, _nodeId ), m_setPointBase( 1 )
{
	SetStaticRequest( StaticRequest_Values );
}

//-----------------------------------------------------------------------------
// <ThermostatSetpoint::ReadXML>
// Read the saved change-counter value
//-----------------------------------------------------------------------------
void ThermostatSetpoint::ReadXML
(
	TiXmlElement const* _ccElement
)
{
	CommandClass::ReadXML( _ccElement );

	int intVal;
	if( TIXML_SUCCESS == _ccElement->QueryIntAttribute( "base", &intVal ) )
	{
		m_setPointBase = (uint8)intVal;
	}
}

//-----------------------------------------------------------------------------
// <ThermostatSetpoint::WriteXML>
// Write the change-counter value
//-----------------------------------------------------------------------------
void ThermostatSetpoint::WriteXML
(
	TiXmlElement* _ccElement
)
{
	CommandClass::WriteXML( _ccElement );

	char str[8];
	snprintf( str, 8, "%d", m_setPointBase );
	_ccElement->SetAttribute( "base", str );
}

//-----------------------------------------------------------------------------
// <ThermostatSetpoint::RequestState>
// Get the static thermostat setpoint details from the device
//-----------------------------------------------------------------------------
bool ThermostatSetpoint::RequestState
(
	uint32 const _requestFlags,
	uint8 const _instance,
	Driver::MsgQueue const _queue
)
{
	bool requests = false;
	if( ( _requestFlags & RequestFlag_Static ) && HasStaticRequest( StaticRequest_Values ) )
	{
		requests |= RequestValue( _requestFlags, 0xff, _instance, _queue );
	}

	if( _requestFlags & RequestFlag_Session )
	{
		for( uint8 i=0; i<ThermostatSetpoint_Count; ++i )
		{
			requests |= RequestValue( _requestFlags, i, _instance, _queue );
		}
	}

	return requests;
}

//-----------------------------------------------------------------------------
// <ThermostatSetpoint::RequestValue>
// Request current state from the device
//-----------------------------------------------------------------------------
bool ThermostatSetpoint::RequestValue
(
	uint32 const _requestFlags,
	uint8 const _setPointIndex,
	uint8 const _instance,
	Driver::MsgQueue const _queue
)
{
	if( _setPointIndex == 0xff )		// check for supportedget
	{
		// Request the supported setpoints
		Msg* msg = new Msg( "ThermostatSetpointCmd_SupportedGet", GetNodeId(), REQUEST, FUNC_ID_ZW_SEND_DATA, true, true, FUNC_ID_APPLICATION_COMMAND_HANDLER, GetCommandClassId() );
		msg->SetInstance( this, _instance );
		msg->Append( GetNodeId() );
		msg->Append( 2 );
		msg->Append( GetCommandClassId() );
		msg->Append( ThermostatSetpointCmd_SupportedGet );
		msg->Append( GetDriver()->GetTransmitOptions() );
		GetDriver()->SendMsg( msg, _queue );
		return true;
	}
	if ( !IsGetSupported() )
	{
		Log::Write(  LogLevel_Info, GetNodeId(), "ThermostatSetpointCmd_Get Not Supported on this node");
		return false;
	}
	Value* value = GetValue( 1, _setPointIndex );
	if( value != NULL )
	{
		value->Release();
		// Request the setpoint value
		Msg* msg = new Msg( "ThermostatSetpointCmd_Get", GetNodeId(), REQUEST, FUNC_ID_ZW_SEND_DATA, true, true, FUNC_ID_APPLICATION_COMMAND_HANDLER, GetCommandClassId() );
		msg->SetInstance( this, _instance );
		msg->Append( GetNodeId() );
		msg->Append( 3 );
		msg->Append( GetCommandClassId() );
		msg->Append( ThermostatSetpointCmd_Get );
		msg->Append( _setPointIndex );
		msg->Append( GetDriver()->GetTransmitOptions() );
		GetDriver()->SendMsg( msg, _queue );
		return true;
	}
	return false;
}

//-----------------------------------------------------------------------------
// <ThermostatSetpoint::HandleMsg>
// Handle a message from the Z-Wave network
//-----------------------------------------------------------------------------
bool ThermostatSetpoint::HandleMsg
(
	uint8 const* _data,
	uint32 const _length,
	uint32 const _instance	// = 1
)
{
	if( ThermostatSetpointCmd_Report == (ThermostatSetpointCmd)_data[0] )
	{
		// We have received a thermostat setpoint value from the Z-Wave device
		if( ValueDecimal* value = static_cast<ValueDecimal*>( GetValue( _instance, _data[1] ) ) )
		{
			uint8 scale;
			uint8 precision = 0;
			string temperature = ExtractValue( &_data[2], &scale, &precision );

			value->SetUnits( scale ? "F" : "C" );
			value->OnValueRefreshed( temperature );
			if( value->GetPrecision() != precision )
			{
				value->SetPrecision( precision );
			}
			value->Release();

			Log::Write( LogLevel_Info, GetNodeId(), "Received thermostat setpoint report: Setpoint %s = %s%s", value->GetLabel().c_str(), value->GetValue().c_str(), value->GetUnits().c_str() );
		}
		return true;
	}

	if( ThermostatSetpointCmd_SupportedReport == (ThermostatSetpointCmd)_data[0] )
	{
		if( Node* node = GetNodeUnsafe() )
		{
			// We have received the supported thermostat setpoints from the Z-Wave device
			Log::Write( LogLevel_Info, GetNodeId(), "Received supported thermostat setpoints" );

			// Parse the data for the supported setpoints
			for( uint32 i=1; i<_length-1; ++i )
			{
				for( int32 bit=0; bit<8; ++bit )
				{
					if( ( _data[i] & (1<<bit) ) != 0 )
					{
						if (GetVersion() >= 3)
						{
							Msg* msg = new Msg("ThermostatSetpointCmd_CapabilitesGet", GetNodeId(), REQUEST, FUNC_ID_ZW_SEND_DATA, true, true, FUNC_ID_APPLICATION_COMMAND_HANDLER, GetCommandClassId());
							msg->SetInstance(this, _instance);
							msg->Append(GetNodeId());
							msg->Append(3);
							msg->Append(GetCommandClassId());
							msg->Append(ThermostatSetpointCmd_CapabilitiesGet);
							uint8 type = ((i - 1) << 3) + bit;
							msg->Append(type);
							msg->Append(GetDriver()->GetTransmitOptions());
							GetDriver()->SendMsg(msg, OpenZWave::Driver::MsgQueue_Query);
							Log::Write(LogLevel_Info, GetNodeId(), "   Requested Thermostat Setpoint Capabilities" );
						}
						// Add supported setpoint
						int32 index = (int32)((i-1)<<3) + bit + m_setPointBase;
						if( index < ThermostatSetpoint_Count )
						{
						  	node->CreateValueDecimal( ValueID::ValueGenre_User, GetCommandClassId(), _instance, index, c_setpointName[index], "C", false, false, "0.0", 0 );
							Log::Write( LogLevel_Info, GetNodeId(), "    Added setpoint: %s", c_setpointName[index] );
						}
					}
				}
			}
		}

		ClearStaticRequest( StaticRequest_Values );
		return true;
	}

	if (ThermostatSetpointCmd_CapabilitiesReport == (ThermostatSetpointCmd) _data[0])
	{
		if (Node* node = GetNodeUnsafe())
		{
			// We have received the capabilities for supported setpoint Type
			uint8 scale;
			uint8 min_precision = 0;
			uint8 max_precision = 0;
			uint8 size = _data[2] & 0x07;
			string minValue = ExtractValue(&_data[2], &scale, &min_precision);
			string maxValue = ExtractValue(&_data[2 + size + 1], &scale, &max_precision);

			Log::Write(LogLevel_Info, GetNodeId(), "Received capabilities of thermostat setpoint type %d, min %s (field size: %i bytes, precision: %i decimals) max %s (precision: %i decimals)", (int) _data[1], minValue.c_str(), size, min_precision, maxValue.c_str(), max_precision);

			uint8 index = _data[1];

// JFD: Porting the Z-TRM3 minsize fix: branch 1.6 has a different way of managing ValueIDs and
// explicitely defines values for setpoint minsize and precision. The index part is 8 bits unsigned
// for both branches. We use an arbitrary unused index value for storing the minsize and precision.
// We don't store the minimum and maximum setpoint values as we have no use for them.            
#define   ValueID_Index_ThermostatSetpoint_SetPointMinSize   250
#define   ValueID_Index_ThermostatSetpoint_SetPointPrecision 251

			if (index < ThermostatSetpoint_Count)
			{
				string setpointName = c_setpointName[index];

				if (m_enforceMinSizePrecision) {
					// Retain the size of the minimum temperature as the minimum field size for the temperature and the minimum precision as the base precision for future communication
					node->CreateValueByte(ValueID::ValueGenre_User, GetCommandClassId(), _instance, ValueID_Index_ThermostatSetpoint_SetPointMinSize, setpointName + "_setpointminsize", "B", false, false, size, 0);
					node->CreateValueByte(ValueID::ValueGenre_User, GetCommandClassId(), _instance, ValueID_Index_ThermostatSetpoint_SetPointPrecision, setpointName + "_setpointprecision", "D", false, false, min_precision, 0);
					Log::Write(LogLevel_Info, GetNodeId(), "EnforceMinSizePrecision enabled, retained min size and min precision from capability report for setpoint command");
				}
//                    node->CreateValueDecimal(ValueID::ValueGenre_User, GetCommandClassId(), _instance, ValueID_Index_ThermostatSetpoint::Unused_0_Minimum + index, setpointName + "_minimum", "C", false, false, minValue, 0);
//                    node->CreateValueDecimal(ValueID::ValueGenre_User, GetCommandClassId(), _instance, ValueID_Index_ThermostatSetpoint::Unused_0_Maximum + index, setpointName + "_maximum", "C", false, false, maxValue, 0);
				Log::Write(LogLevel_Info, GetNodeId(), "    Added setpoint: %s", setpointName.c_str());
			}

		}
	}
	return false;
}

//-----------------------------------------------------------------------------
// <ThermostatSetpoint::SetValue>
// Set a thermostat setpoint temperature
//-----------------------------------------------------------------------------
bool ThermostatSetpoint::SetValue
(
	Value const& _value
)
{
	if( ValueID::ValueType_Decimal == _value.GetID().GetType() )
	{
		ValueDecimal const* value = static_cast<ValueDecimal const*>(&_value);
		uint8 scale = strcmp( "C", value->GetUnits().c_str() ) ? 1 : 0;
		int8 setpointminsize = 0;   // Minimum number of bytes to express the setpoint value, optionally cached from the capabilities report
		int8 setpointprecision = 0; // Minimum precision express the setpoint value, optionally cached from the capabilities report

		if (auto const *minsizeValue = static_cast<ValueByte const*>(GetValue(_value.GetID().GetInstance(),  ValueID_Index_ThermostatSetpoint_SetPointMinSize)))
		{
			setpointminsize = minsizeValue->GetValue();
		}
		if (auto const *precisionValue = static_cast<ValueByte const*>(GetValue(_value.GetID().GetInstance(),  ValueID_Index_ThermostatSetpoint_SetPointPrecision)))
		{
			setpointprecision = precisionValue->GetValue();
		}

		Msg* msg = new Msg( "ThermostatSetpointCmd_Set", GetNodeId(), REQUEST, FUNC_ID_ZW_SEND_DATA, true );
		msg->SetInstance( this, _value.GetID().GetInstance() );
		msg->Append( GetNodeId() );
		msg->Append( 4 + GetAppendValueSize(value->GetValue(), setpointminsize, setpointprecision ) );
		msg->Append( GetCommandClassId() );
		msg->Append( ThermostatSetpointCmd_Set );
		msg->Append( value->GetID().GetIndex() );
		AppendValue( msg, value->GetValue(), scale, setpointminsize, setpointprecision );
		msg->Append( GetDriver()->GetTransmitOptions() );
		GetDriver()->SendMsg( msg, Driver::MsgQueue_Send );
		return true;
	}

	return false;
}

//-----------------------------------------------------------------------------
// <ThermostatSetpoint::CreateVars>
// Create the values managed by this command class
//-----------------------------------------------------------------------------
void ThermostatSetpoint::CreateVars
(
	uint8 const _instance,
	uint8 const _index
)
{
	if( Node* node = GetNodeUnsafe() )
	{
	  	node->CreateValueDecimal( ValueID::ValueGenre_User, GetCommandClassId(), _instance, _index, "Setpoint", "C", false, false, "0.0", 0  );
	}
}
